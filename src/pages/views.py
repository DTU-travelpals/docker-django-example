import os

from django import get_version
from django.conf import settings
from django.shortcuts import render

from .tasks import add_name_to_queue

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
