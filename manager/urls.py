from django.urls import path

from manager.views import (
    index,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
)

urlpatterns = [
    path("", index, name="index"),

    # Task URLs
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),

    # TaskType URLs
    path("task-types/", TaskTypeListView.as_view(), name="task_type-list"),
    path("task-types/create/", TaskTypeCreateView.as_view(), name="task_type-create"),
    path("task-types/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task_type-update"),
    path("task-types/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task_type-delete"),
]

app_name = "manager"
