from services.task_service import TaskService


def show_menu() -> None:
    print("\nTASK MANAGER")
    print("1. Add a task")
    print("2. List tasks")
    print("3. Mark a task as completed")
    print("4. Delete a task")
    print("5. Exit the application")


task_service = TaskService()

while True:
    show_menu()
    try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            task_title = input("Enter the task title: ")
            task = task_service.create_task(task_title)
            print("Task added.")
        elif choice == 2:
            tasks = task_service.list_tasks()
            if not tasks:
                print("No tasks found.")
            else:
                for index, task in enumerate(tasks, start=1):
                    print(f"{index}. {task}")
        elif 3 <= choice <= 4:
            print(f"Your choice: {choice}")
        elif choice == 5:
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
    except ValueError:
        print("Invalid option.")
