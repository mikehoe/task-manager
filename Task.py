from dataclasses import dataclass


@dataclass
class Task:
    task_id: int
    title: str
    completed: bool = False
