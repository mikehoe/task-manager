import pytest

from services.task_service import TaskService


def test_create_task() -> None:
    service = TaskService()

    task = service.create_task("Learn pytest")

    assert task.id == 1
    assert task.title == "Learn pytest"
    assert task.completed is False


def test_create_task_strips_title() -> None:
    service = TaskService()

    task = service.create_task("  Learn pytest  ")

    assert task.title == "Learn pytest"


def test_create_task_with_whitespace_only_title_raises_value_error() -> None:
    service = TaskService()

    with pytest.raises(ValueError, match="Title cannot be empty"):
        service.create_task("   ")


def test_list_tasks_returns_created_tasks() -> None:
    service = TaskService()
    first_task = service.create_task("First task")
    second_task = service.create_task("Second task")

    tasks = service.list_tasks()

    assert tasks == [first_task, second_task]


def test_list_tasks_returns_empty_list_initially() -> None:
    service = TaskService()

    tasks = service.list_tasks()

    assert tasks == []


def test_complete_existing_task() -> None:
    service = TaskService()
    task = service.create_task("Learn pytest")

    result = service.complete_task(task.id)

    assert result is True
    assert task.completed is True


def test_complete_missing_task() -> None:
    service = TaskService()

    result = service.complete_task(999)

    assert result is False


def test_delete_only_task_leaves_empty_list() -> None:
    service = TaskService()
    task = service.create_task("Temporary task")

    result = service.delete_task(task.id)

    assert result is True
    assert service.list_tasks() == []


def test_delete_task_preserves_remaining_tasks() -> None:
    service = TaskService()
    task_to_keep = service.create_task("Keep this task")
    task_to_delete = service.create_task("Delete this task")

    result = service.delete_task(task_to_delete.id)

    assert result is True
    assert service.list_tasks() == [task_to_keep]


def test_delete_missing_task() -> None:
    service = TaskService()

    result = service.delete_task(999)

    assert result is False
