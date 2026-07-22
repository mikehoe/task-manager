import json

from models.task import Task
from persistence.json_storage import JsonStorage


def test_save_and_load_tasks(tmp_path):
    file_path = tmp_path / "tasks.json"
    storage = JsonStorage(str(file_path))

    tasks = [
        Task(id=1, title="Learn pytest", completed=False),
        Task(id=2, title="Write tests", completed=True),
    ]

    storage.save(tasks)
    loaded_tasks = storage.load()

    assert loaded_tasks == tasks


def test_save_writes_expected_json(tmp_path):
    file_path = tmp_path / "tasks.json"
    storage = JsonStorage(str(file_path))

    storage.save([
        Task(id=1, title="Learn pytest", completed=False),
    ])

    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    assert data == [
        {
            "id": 1,
            "title": "Learn pytest",
            "completed": False,
        }
    ]
