from pathlib import Path

import pytest

import cli
from models.task import Task
from persistence.json_storage import JsonStorage
from services.task_service import TaskService


@pytest.fixture
def storage(tmp_path: Path) -> JsonStorage:
    return JsonStorage(tmp_path / "tasks.json")


def test_missing_file_initializes_empty_service(
        storage: JsonStorage,
) -> None:
    service = TaskService(storage.load())

    assert service.list_tasks() == []
    assert service.create_task("First task").id == 1


def test_tasks_survive_service_restart(
        storage: JsonStorage,
) -> None:
    service = TaskService()

    first = service.create_task("Learn Python")
    second = service.create_task("Learn pytest")
    service.complete_task(second.id)

    storage.save(service.list_tasks())

    restored_service = TaskService(storage.load())

    assert restored_service is not service
    assert restored_service.list_tasks() == [
        Task(id=first.id, title="Learn Python", completed=False),
        Task(id=second.id, title="Learn pytest", completed=True),
    ]


@pytest.mark.parametrize(
    "existing_ids, expected_next_id",
    [
        ([], 1),
        ([1], 2),
        ([1, 5, 8], 9),
        ([2, 7], 8),
    ],
)
def test_next_id_is_restored(
        storage: JsonStorage,
        existing_ids: list[int],
        expected_next_id: int,
) -> None:
    tasks = [
        Task(id=task_id, title=f"Task {task_id}")
        for task_id in existing_ids
    ]

    storage.save(tasks)

    restored_service = TaskService(storage.load())
    new_task = restored_service.create_task("New task")

    assert new_task.id == expected_next_id


@pytest.mark.parametrize(
    "operation, expected_tasks",
    [
        (
                "edit",
                [
                    Task(id=1, title="Updated title"),
                    Task(id=2, title="Second task"),
                ],
        ),
        (
                "complete",
                [
                    Task(id=1, title="First task", completed=True),
                    Task(id=2, title="Second task"),
                ],
        ),
        (
                "delete",
                [
                    Task(id=2, title="Second task"),
                ],
        ),
    ],
)
def test_crud_changes_survive_restart(
        storage: JsonStorage,
        operation: str,
        expected_tasks: list[Task],
) -> None:
    service = TaskService()

    first = service.create_task("First task")
    service.create_task("Second task")
    storage.save(service.list_tasks())

    if operation == "edit":
        assert service.edit_task(first.id, "Updated title") is True
    elif operation == "complete":
        assert service.complete_task(first.id) is True
    elif operation == "delete":
        assert service.delete_task(first.id) is True

    storage.save(service.list_tasks())

    restored_service = TaskService(storage.load())

    assert restored_service.list_tasks() == expected_tasks


def test_cli_persists_crud_operations(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    answers = iter([
        "1", "Learn Python",
        "1", "Learn SQL",
        "3", "1",
        "5", "2", "Learn PostgreSQL",
        "4", "1",
        "6",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(answers),
    )

    cli.main()

    storage = JsonStorage(tmp_path / "tasks.json")

    assert storage.load() == [
        Task(
            id=2,
            title="Learn PostgreSQL",
            completed=False,
        )
    ]


def test_cli_loads_saved_tasks_on_restart(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)

    storage = JsonStorage(tmp_path / "tasks.json")
    storage.save([
        Task(id=5, title="Restored task", completed=True)
    ])

    answers = iter(["2", "6"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(answers),
    )

    cli.main()

    output = capsys.readouterr().out

    assert "Restored task" in output
    assert "[x]" in output


@pytest.mark.parametrize(
    "content",
    [
        "{invalid json",
        "{}",
        '[{"id": 1, "title": "Task"}]',
    ],
)
def test_cli_rejects_invalid_saved_data(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
        content: str,
) -> None:
    monkeypatch.chdir(tmp_path)

    file_path = tmp_path / "tasks.json"
    file_path.write_text(content, encoding="utf-8")

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: pytest.fail(
            "CLI must not ask for input after loading fails"
        ),
    )

    cli.main()

    output = capsys.readouterr().out

    assert "Error loading tasks:" in output
    assert "TASK MANAGER" not in output
    assert file_path.read_text(encoding="utf-8") == content


def test_cli_does_not_save_invalid_task(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)

    answers = iter(["1", "   ", "6"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(answers),
    )

    cli.main()

    output = capsys.readouterr().out

    assert "Error: Title cannot be empty" in output
    assert not (tmp_path / "tasks.json").exists()


def test_cli_does_not_save_invalid_edit(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)

    storage = JsonStorage(tmp_path / "tasks.json")
    storage.save([
        Task(id=1, title="Original title")
    ])

    original_content = storage.storage_path.read_bytes()

    answers = iter(["5", "1", "   ", "6"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(answers),
    )

    cli.main()

    output = capsys.readouterr().out

    assert "Error: Title cannot be empty" in output
    assert storage.storage_path.read_bytes() == original_content
    assert storage.load() == [
        Task(id=1, title="Original title")
    ]


def test_cli_exits_when_saving_fails(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)

    def failing_save(self: JsonStorage, tasks: list[Task]) -> None:
        raise PermissionError("Simulated write failure")

    monkeypatch.setattr(JsonStorage, "save", failing_save)

    answers = iter(["1", "New task"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(answers),
    )

    cli.main()

    output = capsys.readouterr().out

    assert "Error saving tasks:" in output
    assert "Simulated write failure" in output
    assert "Task added." not in output
    assert not (tmp_path / "tasks.json").exists()
