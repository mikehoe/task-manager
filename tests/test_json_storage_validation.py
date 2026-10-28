import json
from pathlib import Path

import pytest

from models.task import Task
from persistence.json_storage import JsonStorage


@pytest.fixture
def storage(tmp_path: Path) -> tuple[JsonStorage, Path]:
    file_path = tmp_path / "tasks.json"
    return JsonStorage(file_path), file_path


def write_json(file_path: Path, data: object) -> None:
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file)


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"id": 1, "title": "Learn Python", "completed": False},
        "hello",
        123,
        None,
    ],
)
def test_load_rejects_invalid_root(
        storage: tuple[JsonStorage, Path],
        data: object,
) -> None:
    json_storage, file_path = storage
    write_json(file_path, data)

    with pytest.raises(ValueError, match="JSON root must be a list"):
        json_storage.load()


@pytest.mark.parametrize(
    "item",
    [
        None,
        "task",
        123,
        [],
    ],
)
def test_load_rejects_non_object_items(
        storage: tuple[JsonStorage, Path],
        item: object,
) -> None:
    json_storage, file_path = storage
    write_json(file_path, [item])

    with pytest.raises(ValueError, match="must be an object"):
        json_storage.load()


@pytest.mark.parametrize(
    "data, missing_key",
    [
        ({"title": "Task", "completed": False}, "id"),
        ({"id": 1, "completed": False}, "title"),
        ({"id": 1, "title": "Task"}, "completed"),
    ],
)
def test_load_rejects_missing_keys(
        storage: tuple[JsonStorage, Path],
        data: dict[str, object], missing_key: str,
) -> None:
    json_storage, file_path = storage
    write_json(file_path, [data])

    with pytest.raises(
            ValueError,
            match=f"Missing required key: {missing_key}",
    ):
        json_storage.load()


@pytest.mark.parametrize(
    "task_id",
    [
        0,
        -1,
        "1",
        1.5,
        True,
        False,
        None,
    ],
)
def test_load_rejects_invalid_ids(
        storage: tuple[JsonStorage, Path],
        task_id: object,
) -> None:
    json_storage, file_path = storage

    write_json(file_path, [
        {"id": task_id, "title": "Task", "completed": False}
    ])

    with pytest.raises(
            ValueError,
            match="Task ID must be a positive integer",
    ):
        json_storage.load()


@pytest.mark.parametrize(
    "title",
    [
        "",
        " ",
        "\t",
        "\n",
        123,
        True,
        None,
    ],
)
def test_load_rejects_invalid_titles(
        storage: tuple[JsonStorage, Path],
        title: object,
) -> None:
    json_storage, file_path = storage

    write_json(file_path, [
        {"id": 1, "title": title, "completed": False}
    ])

    with pytest.raises(
            ValueError,
            match="Task title must be a non-empty string",
    ):
        json_storage.load()


@pytest.mark.parametrize(
    "completed",
    [
        "false",
        "true",
        0,
        1,
        None,
    ],
)
def test_load_rejects_invalid_completed_values(
        storage: tuple[JsonStorage, Path],
        completed: object,
) -> None:
    json_storage, file_path = storage

    write_json(file_path, [
        {"id": 1, "title": "Task", "completed": completed}
    ])

    with pytest.raises(
            ValueError,
            match="Task completed must be a boolean",
    ):
        json_storage.load()


def test_load_rejects_duplicate_ids(
        storage: tuple[JsonStorage, Path],
) -> None:
    json_storage, file_path = storage

    write_json(file_path, [
        {"id": 1, "title": "First", "completed": False},
        {"id": 1, "title": "Second", "completed": True},
    ])

    with pytest.raises(ValueError, match="Duplicate task ID: 1"):
        json_storage.load()


def test_load_accepts_valid_tasks(
        storage: tuple[JsonStorage, Path],
) -> None:
    json_storage, file_path = storage

    write_json(file_path, [
        {"id": 1, "title": "Learn Python", "completed": False},
        {"id": 5, "title": "Learn SQL", "completed": True},
    ])

    assert json_storage.load() == [
        Task(id=1, title="Learn Python", completed=False),
        Task(id=5, title="Learn SQL", completed=True),
    ]


def test_load_accepts_empty_list(
        storage: tuple[JsonStorage, Path],
) -> None:
    json_storage, file_path = storage
    write_json(file_path, [])

    assert json_storage.load() == []


def test_load_preserves_json_decode_error(
        storage: tuple[JsonStorage, Path],
) -> None:
    json_storage, file_path = storage
    file_path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        json_storage.load()
