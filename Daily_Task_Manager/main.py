import json
import os
from datetime import datetime

FILE_NAME = "tasks.txt"


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: Tasks file could not be read.")
        return []


def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


def get_next_id(tasks):
    highest_id = 100

    for task in tasks:
        try:
            number = int(task["id"][1:])
            highest_id = max(highest_id, number)
        except (ValueError, KeyError):
            continue

    return f"T{highest_id + 1}"


def add_task(tasks):
    title = input("Enter task title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return

    priority = input(
        "Enter priority (High/Medium/Low): "
    ).strip().capitalize()

    if priority not in ["High", "Medium", "Low"]:
        print("Invalid priority. Enter High, Medium or Low.")
        return

    due_date = input("Enter due date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    task = {
        "id": get_next_id(tasks),
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "status": "Pending"
    }

    tasks.append(task)
    save_tasks(tasks)
    print("Task added.")
    print_task(task)


def print_task(task):
    print(
        f"{task['id']} | {task['title']} | "
        f"{task['priority']} | {task['due_date']} | "
        f"{task['status']}"
    )


def view_by_priority(tasks):
    order = {"High": 1, "Medium": 2, "Low": 3}

    if not tasks:
        print("No tasks found.")
        return

    sorted_tasks = sorted(
        tasks,
        key=lambda task: (
            order.get(task["priority"], 4),
            task["due_date"]
        )
    )

    for task in sorted_tasks:
        print_task(task)


def show_pending(tasks):
    pending = [
        task for task in tasks
        if task["status"] == "Pending"
    ]

    if not pending:
        print("No pending tasks. You are all caught up!")
        return

    for task in pending:
        print_task(task)


def complete_task(tasks):
    task_id = input("Enter task ID to complete: ").strip().upper()

    for task in tasks:
        if task["id"] == task_id:
            if task["status"] == "Done":
                print(f"Task {task_id} is already done.")
                return

            task["status"] = "Done"
            save_tasks(tasks)

            pending_count = sum(
                1 for item in tasks
                if item["status"] == "Pending"
            )

            print(
                f"Task {task_id} marked as done. "
                f"Pending tasks: {pending_count}"
            )
            return

    print(f"Task {task_id} not found.")


def main():
    tasks = load_tasks()

    while True:
        print("\n===== DAILY TASK MANAGER =====")
        print("1. Add task")
        print("2. View by priority")
        print("3. Show pending tasks")
        print("4. Complete task")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_by_priority(tasks)
        elif choice == "3":
            show_pending(tasks)
        elif choice == "4":
            complete_task(tasks)
        elif choice == "5":
            print("Tasks saved. Goodbye!")
            break
        else:
            print("Invalid menu option. Enter 1 to 5.")


if __name__ == "__main__":
    main()