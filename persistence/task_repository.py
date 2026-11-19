from typing import Protocol

from models.task import Task


class TaskRepository(Protocol):

    def create(self, title: str) -> Task:
        ...

    def get_by_id(self, task_id: int) -> Task | None:
        ...

    def list_all(self) -> list[Task]:
        ...

    def delete(self, task_id: int) -> bool:
        ...

    def update(self, task: Task) -> bool:
        ...
