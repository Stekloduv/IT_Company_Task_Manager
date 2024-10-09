from django import forms
from manager.models import Task, TaskType, Position


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ['name']


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']