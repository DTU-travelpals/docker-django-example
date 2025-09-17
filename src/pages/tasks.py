import json

import redis
from celery import shared_task


@shared_task
def add_name_to_queue(name):
    # For now, we'll just print the name to the console.
    # In a real application, you might do something more complex here.
    print(f"Received name: {name}")
    return f"{name}"


def read_tasks_from_db(settings):
    r = redis.from_url(settings.REDIS_URL)
    task_keys = r.keys("celery-task-meta-*")
    tasks = []
    for key in task_keys:
        task_data = r.get(key)
        if task_data:
            tasks.append(json.loads(task_data))

    # Sort tasks by date_done, newest first. Handle tasks without date_done.
    tasks.sort(key=lambda x: x.get("date_done") or "", reverse=True)

    return tasks


def update_task_in_db(settings, task_id, data_to_update):
    r = redis.from_url(settings.REDIS_URL)
    key = f"celery-task-meta-{task_id}"
    task_data = r.get(key)
    if task_data:
        task = json.loads(task_data)
        task.update(data_to_update)
        r.set(key, json.dumps(task))
