"""Small interactive console demo for laboratory work 3, variant 15."""

from core import (
    add_comment,
    add_label,
    change_priority,
    change_status,
    create_example_task,
    task_summary,
)
from model import Comment


def main() -> None:
    task = create_example_task()
    next_comment_id = 1

    while True:
        print("\\n=== PROJECT TASK SYSTEM (variant 15) ===")
        print("1. Show task")
        print("2. Add comment")
        print("3. Add label")
        print("4. Change status")
        print("5. Change priority")
        print("0. Exit")
        choice = input("Choose an action: ").strip()

        try:
            if choice == "1":
                print(task_summary(task))
                print("Description:", task.description)
                print("Labels:", ", ".join(sorted(task.labels)) or "(none)")
                print("Comments:")
                for comment in task.comments:
                    print(f"  [{comment.id}] {comment.author}: {comment.text}")
                print("Metadata:", dict(task.metadata))
            elif choice == "2":
                author = input("Author: ").strip()
                text = input("Comment: ").strip()
                if not author or not text:
                    print("Author and comment cannot be empty.")
                    continue
                comment = Comment(next_comment_id, author, text, "2026-11-03")
                task = add_comment(task, comment)
                next_comment_id += 1
                print("A new task version has been created.")
            elif choice == "3":
                task = add_label(task, input("Label: "))
                print("A new task version has been created.")
            elif choice == "4":
                print("Available statuses: todo, in_progress, done, blocked")
                task = change_status(task, input("New status: ").strip())
                print("A new task version has been created.")
            elif choice == "5":
                task = change_priority(task, int(input("New priority (1-5): ")))
                print("A new task version has been created.")
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Unknown menu item.")
        except (ValueError, TypeError) as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
