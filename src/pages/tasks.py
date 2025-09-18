import json
from datetime import datetime

import redis
from celery import shared_task


@shared_task
def add_name_to_queue(name):
    # For now, we'll just print the name to the console.
    # In a real application, you might do something more complex here.
    print(f"Received name: {name}")
    return f"{name}"


def read_tasks_from_db(
    settings, sort_by="date_done", sort_order="desc", tasks=None
):
    if tasks is None:
        r = redis.from_url(settings.REDIS_URL)
        task_keys = r.keys("celery-task-meta-*")
        tasks = []
        for key in task_keys:
            task_data = r.get(key)
            if task_data:
                tasks.append(json.loads(task_data))

    # Sorting logic
    reverse = sort_order == "desc"

    def sort_key(task):
        value = task.get(sort_by)

        if value is None:
            # For dates, we can use a min datetime object for None values
            if sort_by == "date_done":
                return datetime.min
            # For other types, an empty string is a reasonable default
            return ""

        if sort_by == "date_done":
            if not value:
                return datetime.min
            try:
                # Celery uses ISO 8601 format for dates
                return datetime.fromisoformat(value)
            except (TypeError, ValueError):
                # Fallback for invalid date formats
                return datetime.min

        # For other columns, we can return the value as is
        return value

    tasks.sort(key=sort_key, reverse=reverse)

    return tasks


def update_task_in_db(settings, task_id, data_to_update):
    r = redis.from_url(settings.REDIS_URL)
    key = f"celery-task-meta-{task_id}"
    task_data = r.get(key)
    if task_data:
        task = json.loads(task_data)
        task.update(data_to_update)
        r.set(key, json.dumps(task))
