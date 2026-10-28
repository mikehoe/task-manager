import json
from pathlib import Path

import pytest

from models.task import Task
from persistence.json_storage import JsonStorage


@pytest.fixture
def storage(tmp_path: Path) -> tuple[JsonStorage, Path]:
    file_path = tmp_path / "tasks.json"

    return JsonStorage(file_path), file_path


def test_save_and_load_tasks(
        storage: tuple[JsonStorage, Path],
) -> None:
    json_storage, _ = storage

    tasks = [
        Task(id=1, title="Learn pytest", completed=False),
        Task(id=2, title="Write tests", completed=True),
    ]

    json_storage.save(tasks)

    assert json_storage.load() == tasks


def test_load_returns_empty_list_when_file_does_not_exist(
        storage: tuple[JsonStorage, Path],
) -> None:
    json_storage, _ = storage

    assert json_storage.load() == []


def test_load_raises_error_when_json_is_invalid(
        storage: tuple[JsonStorage, Path],
) -> None:
    json_storage, file_path = storage

    file_path.write_text('{"id": 1, "title": "Broken"', encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        json_storage.load()


def test_save_writes_expected_json(
        storage: tuple[JsonStorage, Path],
) -> None:
    json_storage, file_path = storage

    json_storage.save([
        Task(
            id=1,
            title="Learn Python",
            completed=False,
        ),
    ])

    with file_path.open("r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    assert data == [
        {
            "id": 1,
            "title": "Learn Python",
            "completed": False,
        }
    ]


def test_save_removes_temporary_file_after_success(
        storage: tuple[JsonStorage, Path],
) -> None:
    json_storage, file_path = storage

    temporary_path = file_path.with_suffix(
        file_path.suffix + ".tmp"
    )

    json_storage.save([
        Task(id=1, title="Test task", completed=False),
    ])

    assert file_path.exists()
    assert not temporary_path.exists()


def test_save_preserves_original_file_when_replacement_fails(
        storage: tuple[JsonStorage, Path],
        monkeypatch: pytest.MonkeyPatch,
) -> None:
    json_storage, file_path = storage

    original_tasks = [
        Task(id=1, title="Original task", completed=False),
    ]

    json_storage.save(original_tasks)

    def raise_os_error(*args: object, **kwargs: object) -> None:
        raise OSError("Simulated replacement failure")

    monkeypatch.setattr(Path, "replace", raise_os_error)

    new_tasks = [
        Task(id=2, title="New task", completed=True),
    ]

    with pytest.raises(OSError, match="Simulated replacement failure"):
        json_storage.save(new_tasks)

    temporary_path = file_path.with_suffix(
        file_path.suffix + ".tmp"
    )

    assert not temporary_path.exists()
    assert json_storage.load() == original_tasks
