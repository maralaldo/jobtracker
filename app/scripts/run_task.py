import sys
from app.tasks.vacancies import parse_vacancies
from app.tasks.notifications import send_notifications


TASKS = {
    "parse_vacancies": parse_vacancies,
    "send_notifications": send_notifications,
}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python -m app.scripts.run_task <task_name>")
        print(f"Available tasks: {list(TASKS.keys())}")
        sys.exit(1)

    task_name = sys.argv[1]
    if task_name not in TASKS:
        print(f"❌ Unknown task: {task_name}")
        print(f"Available tasks: {list(TASKS.keys())}")
        sys.exit(1)

    task = TASKS[task_name]
    result = task.delay()
    print(f"✅ Task {task_name} sent to Celery. Task ID = {result.id}")
