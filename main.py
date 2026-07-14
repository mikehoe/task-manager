def show_menu() -> None:
    print("\nTASK MANAGER")
    print("1. Add a task")
    print("2. List tasks")
    print("3. Mark a task as completed")
    print("4. Delete a task")
    print("5. Exit the application")

while True:
    show_menu()
    try:
        choice = int(input("Enter your choice: "))
        if 1 <= choice <= 4:
            print(f"Your choice: {choice}")
        elif choice == 5:
            break
        else:
            print("Invalid option")
    except ValueError:
        print("Invalid option")
