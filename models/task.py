from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    completed: bool = False

    def __str__(self) -> str:
        return f"{self.title}"
