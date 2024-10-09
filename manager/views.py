from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from manager.models import Worker, Task, TaskType, Position


def index(request):
    """View function for the home page of the site."""

    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "manager/index.html", context=context)


class TaskTypeListView(generic.ListView):
    model = TaskType
    context_object_name = "TaskType_list_list"
    template_name = "manager/task_type_list.html"
    paginate_by = 5


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("manager:task_type-list")


class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("manager:task_type-list")


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("manager:task_type-list")


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 5
    queryset = Task.objects.all().select_related("task_type")


class TaskDetailView(generic.DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        context["is_worker"] = self.request.user in car.workers.all()
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        car = self.get_object()
        user = request.user

        if "assign" in request.POST:
            car.drivers.add(user)
        elif "delete" in request.POST:
            car.drivers.remove(user)

        return redirect("taxi:task-detail", pk=task.pk)


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("taxi:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    success_url = reverse_lazy("taxi:task-list")
    form_class = TaskForm


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("taxi:task-list")


class PositionListView(generic.ListView):
    model = Position
    context_object_name = "position_list"
    template_name = "manager/position_list.html"
    paginate_by = 5


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    template_name = "manager/position_form.html"
    success_url = reverse_lazy("manager:position-list")


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    template_name = "manager/position_form.html"
    success_url = reverse_lazy("manager:position-list")


class PositionDeleteView(generic.DeleteView):
    model = Position
    template_name = "manager/position_confirm_delete.html"
    success_url = reverse_lazy("manager:position-list")



