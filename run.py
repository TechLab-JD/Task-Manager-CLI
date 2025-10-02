
# Task Manager CLI
# Clean, robust, and user-friendly
from data.util.task_manager import Task
from rich.console import Console
from rich.table import Table
import json
from datetime import datetime

console = Console()

def load_tasks():
    """Load tasks from the JSON file."""
    try:
        with open("data/tasks.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def display_tasks(tasks):
    """Display all tasks in a colorful table."""
    table = Table(title="Task Manager   \n\t\t\t  By: Dr.Glitch404", show_lines=True)
    table.add_column("ID", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Title", style="magenta")
    table.add_column("Description", style="purple")    
    table.add_column("Priority", style="yellow")
    table.add_column("Due Date", style="red")
    table.add_column("Created At", style="blue")
    table.add_column("Updated On", style="white")

    from datetime import datetime
    def fmt(dt):
        if not dt:
            return ""
        try:
            return datetime.fromisoformat(dt).strftime("%Y-%m-%d %H:%M")
        except Exception:
            return dt

    for task in tasks:
        status = "✔️" if task.get("status") else "❌"
        priority = task.get("priority", "")
        if priority == "high":
            priority_color = "bold red"
        elif priority == "medium":
            priority_color = "bold yellow"
        else:
            priority_color = "bold green"
        table.add_row(
            str(task.get("id", ""))[:3],
            status,
            task.get("title", ""),
            task.get("description", ""),
            f"[{priority_color}]{priority}[/{priority_color}]",
            task.get("due_date", ""),
            fmt(task.get("created_at", "")),
            fmt(task.get("updated_on", ""))
        )
    console.clear()
    console.print(table)

def add_task():
    """Prompt user for task details and add a new task."""
    title = input("Enter task title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    description = input("Enter description (optional): ").strip()
    priority = input("Priority (low/medium/high): ").strip().lower()
    if priority not in ["low", "medium", "high"]:
        print("Invalid priority. Defaulting to 'low'.")
        priority = "low"
    due_date = input("Due date (optional): ").strip()
    # Generate a 3-character ID
    task_id = str(int(datetime.utcnow().timestamp()))[-3:]
    task = Task(id=task_id, title=title, description=description, priority=priority, due_date=due_date)
    task.save()
    print("Task added!")

def main():
    while True:
        tasks = load_tasks()
        display_tasks(tasks)
        print("[A]dd [E]dit [D]elete [Q]uit")
        choice = input("Choose an action: ").strip().lower()
        if choice == "a":
            add_task()
        elif choice == "e":
            task_id = input("Enter task ID to edit: ")[:3]
            for t in tasks:
                if str(t["id"])[-3:] == task_id:
                    task = Task(**t)
                    edited = False
                    while True:
                        change = input("Change (t)itle, (d)escription, (p)riority, (s)tatus, (due) date or (q)uit: ").strip().lower()
                        if change == "q":
                            if edited:
                                confirm = input("Confirm all changes and save? (y/n): ").strip().lower()
                                if confirm == "y":
                                    task.save()
                                    print("Task updated!")
                                else:
                                    print("No changes saved.")
                            else:
                                print("Edit cancelled.")
                            break
                        elif change == "t":
                            new_title = input(f"New title (current: {task.title}): ").strip()
                            if new_title:
                                task.title = new_title
                                edited = True
                        elif change == "d":
                            new_description = input(f"New description (current: {task.description}): ").strip()
                            task.description = new_description
                            edited = True
                        elif change == "p":
                            new_priority = input(f"New priority (current: {task.priority}) [high, medium, low]: ").strip().lower()
                            if new_priority in ["low", "medium", "high"]:
                                task.set_priority(new_priority)
                                edited = True
                            else:
                                print("Invalid priority. No change made.")
                        elif change == "due":
                            new_due_date = input(f"New due date (current: {task.due_date}): ").strip()
                            task.due_date = new_due_date
                            edited = True
                        elif change == "s":
                            new_status = input(f"Is the task complete? (y/n, current: {'yes' if task.status else 'no'}): ").strip().lower()
                            if new_status == "y":
                                task.mark_complete()
                                edited = True
                            elif new_status == "n":
                                task.mark_incomplete()
                                edited = True
                        else:
                            print("Invalid option.")
                            continue
                        more = input("Edit another field? (y/n): ").strip().lower()
                        if more != "y":
                            confirm = input("Confirm all changes and save? (y/n): ").strip().lower()
                            if confirm == "y":
                                task.save()
                                print("Task updated!")
                            else:
                                print("No changes saved.")
                            break
                    break
            else:
                print("Task ID not found.")
        elif choice == "d":
            task_id = input("Enter task ID to delete: ")[:3]
            for t in tasks:
                if str(t["id"])[-3:] == task_id:
                    confirm = input(f"Are you sure you want to delete task '{t['title']}'? (y/n): ").strip().lower()
                    if confirm == "y":
                        tasks.remove(t)
                        with open("data/tasks.json", "w", encoding="utf-8") as f:
                            json.dump(tasks, f, indent=2)
                        print("Task deleted!")
                    else:
                        print("Delete cancelled.")
                    break
            else:
                print("Task ID not found.")
        elif choice == "q":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()


