from models.task import Task


def valid_task_title(title: str) -> str:
    title = title.strip()

    if not title:
        raise ValueError("Title cannot be empty")

    return title


class TaskService:

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def create_task(self, title: str) -> Task:
        task = Task(id=self._next_id, title=valid_task_title(title))
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

    def delete_task(self, task_id: int) -> bool:
        if task_id not in self._tasks:
            return False
        self._tasks.pop(task_id)
        return True

    def edit_task(self, task_id: int, new_title: str) -> bool:
        if task_id not in self._tasks:
            return False
        task = self._tasks[task_id]
        task.title = valid_task_title(new_title)
        return True
