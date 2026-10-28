import json
from pathlib import Path

from models.task import Task


class JsonStorage:
    def __init__(self, storage_path: str | Path):
        self.storage_path = Path(storage_path)

    def save(self, tasks: list[Task]) -> None:
        temporary_path = self.storage_path.with_suffix(
            self.storage_path.suffix + ".tmp"
        )

        serialized_tasks = [self._task_to_dict(task) for task in tasks]

        try:
            with temporary_path.open("w", encoding="utf-8") as json_file:
                json.dump(
                    serialized_tasks,
                    json_file,
                    indent=4,
                    ensure_ascii=False,
                )

            temporary_path.replace(self.storage_path)

        finally:
            if temporary_path.exists():
                temporary_path.unlink()

    def load(self) -> list[Task]:
        try:
            with self.storage_path.open("r", encoding="utf-8") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            return []

        if not isinstance(data, list):
            raise ValueError("JSON root must be a list")

        tasks = []
        seen_ids = set()

        for index, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(
                    f"Task at index {index} must be an object"
                )

            task = self._dict_to_task(item)

            if task.id in seen_ids:
                raise ValueError(f"Duplicate task ID: {task.id}")

            seen_ids.add(task.id)
            tasks.append(task)

        return tasks

    @staticmethod
    def _task_to_dict(task: Task) -> dict[str, int | str | bool]:
        return {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
        }

    @staticmethod
    def _dict_to_task(data: dict) -> Task:
        required_keys = ("id", "title", "completed")

        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key: {key}")

        task_id = data["id"]
        title = data["title"]
        completed = data["completed"]

        if type(task_id) is not int or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title must be a non-empty string")

        if not isinstance(completed, bool):
            raise ValueError("Task completed must be a boolean")

        return Task(
            id=task_id,
            title=title,
            completed=completed,
        )
