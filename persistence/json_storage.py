import json

from models.task import Task


class JsonStorage:

    def __init__(self, storage_path: str):
        self.storage_path = storage_path

    def save(self, tasks: list[Task]) -> None:
        with open(self.storage_path, "w") as json_file:
            json.dump(
                [self._task_to_dict(task) for task in tasks],
                json_file,
                indent=4,
            )

    def load(self) -> list[Task]:
        with open(self.storage_path, "r") as json_file:
            data = json.load(json_file)

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
