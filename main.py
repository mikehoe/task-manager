from models.task import Task
from services.task_service import TaskService


def show_menu() -> None:
    print("\nTASK MANAGER")
    print("1. Add a task")
    print("2. List tasks")
    print("3. Mark a task as completed")
    print("4. Delete a task")
    print("5. Exit the application")


def show_tasks(tasks: list[Task]) -> None:
    if not tasks:
        print("No tasks found.")
    else:
        for index, task in enumerate(tasks, start=1):
            print(f"{index}. {"[x]" if task.completed else "[ ]"} {task}")


def main() -> None:
    task_service = TaskService()

    while True:
        show_menu()

        choice = input("Enter your choice: ").strip()

        match choice:
            case "1":
                task_title = input("Enter the task title: ")
                try:
                    task_service.create_task(task_title)
                    print("Task added.")
                except ValueError as error:
                    print(f"Error: {error}")

            case "2":
                show_tasks(task_service.list_tasks())

            case "3":
                tasks = task_service.list_tasks()
                show_tasks(tasks)

                try:
                    selected_number = int(input("Enter the number of the task to complete: "))
                    selected_task = tasks[selected_number - 1]
                    if task_service.complete_task(selected_task.id):
                        print(f"Task {selected_number}. {selected_task} completed!")
                    else:
                        print("Task not found.")
                except ValueError:
                    print("Invalid choice! Please enter a number.")
                except IndexError:
                    print("Invalid task number! Please enter a number from list of tasks if there any.")

            case "4":
                print(f"Your choice: {choice}")

            case "5":
                print("Goodbye!")
                break

            case _:
                print("Invalid option! Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
