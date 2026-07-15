from models.task import Task


class TaskService:
    _tasks: list[Task]
    _next_id: int

    def __init__(self) -> None:
        self._tasks = []
        self._next_id = 1

    def create_task(self, title: str) -> Task:
        task = Task(id=self._next_id, title=title)
        self._next_id += 1
        self._tasks.append(task)
        return task

    def list_tasks(self) -> list[Task]:
        return self._tasks.copy()
