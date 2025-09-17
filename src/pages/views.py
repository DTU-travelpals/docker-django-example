import json
import os

from django import get_version
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .tasks import add_name_to_queue, read_tasks_from_db, update_task_in_db


def home(request):
    if request.method == "POST":
        name = request.POST.get("name", "Anonymous")
        add_name_to_queue.delay(name)
        context = {
            "message": f"Hello {name}, your name has been added to the queue!",
            "debug": settings.DEBUG,
            "django_ver": get_version(),
            "python_ver": os.environ["PYTHON_VERSION"],
        }
        return render(request, "pages/home.html", context)

    context = {
        "debug": settings.DEBUG,
        "django_ver": get_version(),
        "python_ver": os.environ["PYTHON_VERSION"],
    }

    return render(request, "pages/home.html", context)


def task_list(request):
    context = {
        "tasks": read_tasks_from_db(settings),
    }

    return render(request, "pages/tasks.html", context)


@require_POST
def update_task_status(request):
    try:
        data = json.loads(request.body)
        task_id = data.get("task_id")
        completed = data.get("completed")

        if task_id is None or completed is None:
            return JsonResponse(
                {"success": False, "error": "Missing parameters"}, status=400
            )

        update_task_in_db(settings, task_id, {"completed": completed})

        return JsonResponse({"success": True})
    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid JSON"}, status=400
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
