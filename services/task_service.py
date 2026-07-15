from models.task import Task


class TaskService:

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def create_task(self, title: str) -> Task:
        title = title.strip()

        if not title:
            raise ValueError("Title cannot be empty")

        task = Task(id=self._next_id, title=title)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def list_tasks(self) -> list[Task]:
        return list(self._tasks.values())

    def complete_task(self, task_id: int) -> bool:
        if task_id not in self._tasks:
            return False
        task = self._tasks[task_id]
        task.completed = True
        return True
