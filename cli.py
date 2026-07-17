from models.task import Task
from services.task_service import TaskService

task_service = TaskService()


def separator() -> str:
    return "-" * 80


def show_menu() -> None:
    print(f"{separator()}\nTASK MANAGER\n{separator()}")
    print("1. Add a task")
    print("2. List tasks")
    print("3. Mark a task as completed")
    print("4. Delete a task")
    print("5. Exit the application")


def show_tasks() -> bool:
    tasks = task_service.list_tasks()

    if not tasks:
        print("No tasks found.")
        return False

    for index, task in enumerate(tasks, start=1):
        status = "[x]" if task.completed else "[ ]"
        print(f"{index}. {status} {task}")

    return True


def select_task() -> Task | None:
    try:
        selected_number = int(input("Enter a number of the task: "))
    except ValueError:
        print("Invalid choice! Please enter a number.")
        return None

    tasks = task_service.list_tasks()

    if selected_number < 1 or selected_number > len(tasks):
        print("Invalid task number! Please enter a number from the list.")
        return None

    return tasks[selected_number - 1]


def main() -> None:
    while True:
        show_menu()
        choice = input("Enter a number of your choice: ").strip()

        match choice:
            case "1":
                print(f"{separator()}\nAdd a task\n{separator()}")

                task_title = input("Enter a task title: ")
                try:
                    task_service.create_task(task_title)
                    print("Task added.")
                except ValueError as error:
                    print(f"Error: {error}")

            case "2":
                print(f"{separator()}\nList tasks\n{separator()}")

                show_tasks()

            case "3":
                print(f"{separator()}\nMark a task as completed\n{separator()}")

                if not show_tasks():
                    continue

                selected_task = select_task()

                if selected_task is None:
                    continue

                if task_service.complete_task(selected_task.id):
                    print(f"Task {selected_task} completed!")
                else:
                    print("Task not found.")

            case "4":
                print(f"{separator()}\nDelete a task\n{separator()}")

                if not show_tasks():
                    continue

                selected_task = select_task()

                if selected_task is None:
                    continue

                if task_service.delete_task(selected_task.id):
                    print(f"Task {selected_task} deleted!")
                else:
                    print("Task not found.")

            case "5":
                print("Goodbye!")
                break

            case _:
                print("Invalid option! Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
