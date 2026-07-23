import json
from pathlib import Path

from models.task import Task


class JsonStorage:
    def __init__(self, storage_path: str | Path):
        self.storage_path = Path(storage_path)

        if not self.storage_path.suffix:
            self.storage_path = self.storage_path / "tasks.json"

    def save(self, tasks: list[Task]) -> None:
        tmp_path = self.storage_path.with_suffix(self.storage_path.suffix + ".tmp")

        try:
            serialized_tasks = [self._task_to_dict(task) for task in tasks]

            with tmp_path.open("w", encoding="utf-8") as json_file:
                json.dump(serialized_tasks, json_file, indent=4, ensure_ascii=False)

            tmp_path.replace(self.storage_path)

        except (OSError, TypeError, AttributeError) as error:
            print(f"ERROR: Failed to save tasks safely.\n{error}")

            if tmp_path.exists():
                tmp_path.unlink()

    def load(self) -> list[Task]:
        try:
            with self.storage_path.open("r", encoding="utf-8") as json_file:
                data = json.load(json_file)
        except FileNotFoundError as error:
            print(f"[DEBUG]: File not found, creating an empty list.\n{error}")
            return []
        except json.JSONDecodeError as error:
            print(f"WARNING: File {self.storage_path} is damaged.\n{error}")
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
