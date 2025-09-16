from celery import shared_task


@shared_task
def add_name_to_queue(name):
    # For now, we'll just print the name to the console.
    # In a real application, you might do something more complex here.
    print(f"Received name: {name}")
    return f"Hello, {name}!"
