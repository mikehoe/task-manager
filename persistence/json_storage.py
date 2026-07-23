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
        except FileNotFoundError as error:
            return []

        return [self._dict_to_task(item) for item in data]

    @staticmethod
    def _task_to_dict(task: Task) -> dict[str, int | str | bool]:
        return {
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
        }

    @staticmethod
    def _dict_to_task(data: dict) -> Task:
        return Task(
            id=data["id"],
            title=data["title"],
            completed=data["completed"],
        )
