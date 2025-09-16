from django.urls import path

from pages import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tasks/", views.task_list, name="tasks"),
]
