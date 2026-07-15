def show_menu() -> None:
    print("\nTASK MANAGER")
    print("1. Add a task")
    print("2. List tasks")
    print("3. Mark a task as completed")
    print("4. Delete a task")
    print("5. Exit the application")


tasks = []

while True:
    show_menu()
    try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            task_title = input("Enter the task title: ")
            tasks.append(task_title)
            print("Task added.")
        if choice == 2:
            if not tasks:
                print("No tasks found.")
            else:
                for index, task in enumerate(tasks):
                    print(f"{index + 1}. {task}")
        elif 3 <= choice <= 4:
            print(f"Your choice: {choice}")
        elif choice == 5:
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
    except ValueError:
        print("Invalid option.")
