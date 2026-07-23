import json
from pathlib import Path

import pytest

from models.task import Task
from persistence.json_storage import JsonStorage


@pytest.fixture
def test_storage(tmp_path) -> tuple[JsonStorage, Path]:
    file_path = tmp_path / "tasks.json"
    storage = JsonStorage(file_path)
    return storage, file_path


def test_save_and_load_tasks_success(test_storage):
    storage, _ = test_storage
    tasks = [
        Task(id=1, title="Learn pytest", completed=False),
        Task(id=2, title="Write tests", completed=True),
    ]

    storage.save(tasks)
    loaded_tasks = storage.load()

    # Thanks to @dataclass this content comparison works perfectly
    assert loaded_tasks == tasks


def test_load_file_not_found(test_storage):
    storage, _ = test_storage
    loaded_tasks = storage.load()

    assert loaded_tasks == []


def test_load_damaged_json(test_storage):
    storage, file_path = test_storage

    # Write invalid JSON to the file (closing bracket is missing)
    file_path.write_text('{"id": 1, "title": "Broken"', encoding="utf-8")

    loaded_tasks = storage.load()

    assert loaded_tasks == []


def test_save_creates_atomic_tmp_file_and_cleans_up(test_storage):
    """Ověří, že save() po sobě nezanechá žádný dočasný soubor .tmp."""
    storage, file_path = test_storage
    tasks = [Task(id=1, title="Atomic test", completed=False)]
    tmp_path = file_path.with_suffix(file_path.suffix + ".tmp")

    storage.save(tasks)

    assert file_path.exists()
    assert not tmp_path.exists()


def test_save_handles_serialization_error_and_cleans_up(test_storage, monkeypatch):
    """
    Ověří, že pokud selže serializace (např. TypeError),
    původní data zůstanou v bezpečí a dočasný .tmp soubor se uklidí.
    """
    storage, file_path = test_storage

    # 1. First we save some valid data
    valid_tasks = [Task(id=1, title="Valid task", completed=False)]
    storage.save(valid_tasks)

    # 2. We simulate a serialization error by pushing an invalid object,
    # which json.dump cannot process (e.g. the Path object itself)
    bad_tasks = [Path("/invalid/object")]  # Vyvolá TypeError při json.dump

    storage.save(bad_tasks)

    # 3. Verification: The temporary file must not remain on the disk
    tmp_path = file_path.with_suffix(file_path.suffix + ".tmp")
    assert not tmp_path.exists()

    # 4. The original valid data in the file had to remain intact
    assert storage.load() == valid_tasks


def test_save_writes_expected_json(test_storage):
    storage, file_path = test_storage

    storage.save([
        Task(id=1, title="Learn pytest", completed=False),
    ])

    with file_path.open("r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    assert data == [
        {
            "id": 1,
            "title": "Learn pytest",
            "completed": False,
        }
    ]
