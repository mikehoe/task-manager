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
            task = input("Enter the task title: ")
            tasks.append(task)
            print("Task added.")
        elif 2 <= choice <= 4:
            print(f"Your choice: {choice}")
        elif choice == 5:
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
    except ValueError:
        print("Invalid option.")
