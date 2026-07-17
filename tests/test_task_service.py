import pytest

from services.task_service import TaskService


@pytest.fixture
def service() -> TaskService:
    return TaskService()


def test_create_task(service: TaskService) -> None:
    task = service.create_task("Learn pytest")

    assert task.id == 1
    assert task.title == "Learn pytest"
    assert task.completed is False


def test_create_task_strips_title(service: TaskService) -> None:
    task = service.create_task("  Learn pytest  ")

    assert task.title == "Learn pytest"


@pytest.mark.parametrize("title", ["", " ", "   ", "\t", "\n"])
def test_invalid_titles_raise_value_error(service: TaskService, title: str) -> None:
    with pytest.raises(ValueError, match="Title cannot be empty"):
        service.create_task(title)


def test_list_tasks_returns_created_tasks(service: TaskService) -> None:
    first_task = service.create_task("First task")
    second_task = service.create_task("Second task")

    tasks = service.list_tasks()

    assert tasks == [first_task, second_task]


def test_list_tasks_returns_empty_list_initially(service: TaskService) -> None:
    tasks = service.list_tasks()

    assert tasks == []


def test_complete_existing_task(service: TaskService) -> None:
    task = service.create_task("Learn pytest")

    result = service.complete_task(task.id)

    assert result is True
    assert task.completed is True


def test_complete_missing_task(service: TaskService) -> None:
    result = service.complete_task(999)

    assert result is False


def test_delete_only_task_leaves_empty_list(service: TaskService) -> None:
    task = service.create_task("Temporary task")

    result = service.delete_task(task.id)

    assert result is True
    assert service.list_tasks() == []


def test_delete_task_preserves_remaining_tasks(service: TaskService) -> None:
    task_to_keep = service.create_task("Keep this task")
    task_to_delete = service.create_task("Delete this task")

    result = service.delete_task(task_to_delete.id)

    assert result is True
    assert service.list_tasks() == [task_to_keep]


def test_delete_missing_task(service: TaskService) -> None:
    result = service.delete_task(999)

    assert result is False
