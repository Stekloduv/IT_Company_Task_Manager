from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from manager.models import Task, TaskType, Position

TASKS_URL = reverse("manager:task-list")


class PublicTaskTests(TestCase):
    def setUp(self) -> None:
        task_type = TaskType.objects.create(
            name="test777"
        )
        self.task = Task.objects.create(
            name="test12345",
            description="About task",
            deadline=now(),
            task_type=task_type
        )

    def test_task_list_login_required(self):
        response = self.client.get(TASKS_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_task_create_login_required(self):
        response = self.client.get(reverse("manager:task-create"))

        self.assertNotEqual(response.status_code, 200)

    def test_task_update_login_required(self):
        response = self.client.get(reverse(
            "manager:task-update", kwargs={"pk": self.task.id}
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_task_delete_login_required(self):
        response = self.client.get(reverse(
            "manager:task-delete", kwargs={"pk": self.task.id}
        ))

        self.assertNotEqual(response.status_code, 200)


class PrivateTaskTests(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(
            name="test778"
        )
        self.position = Position.objects.create(name="red")
        self.task = Task.objects.create(
            name="test12345",
            description="About task",
            deadline=now(),
            task_type=self.task_type
        )
        number_of_tasks = 12

        for task in range(2, number_of_tasks):
            task_type = TaskType.objects.create(
                name=f"{task}task"
            )

            Task.objects.create(
                name=f"test12345{task}",
                description=f"About task{task}",
                deadline=now(),
                task_type=task_type
            )

        self.queryset = Task.objects.all()

        self.worker = get_user_model().objects.create_user(
            username="test",
            password="password123",
            position=self.position
        )
        self.client.force_login(self.worker)

    def test_task_list_login_required(self):
        response = self.client.get(TASKS_URL)

        self.assertEqual(response.status_code, 200)

    def test_task_create_login_required(self):
        response = self.client.get(reverse("manager:task-create"))

        self.assertEqual(response.status_code, 200)

    def test_task_update_login_required(self):
        response = self.client.get(reverse(
            "manager:task-update", kwargs={"pk": self.task.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_task_delete_login_required(self):
        response = self.client.get(reverse(
            "manager:task-delete", kwargs={"pk": self.task.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_retrieve_tasks(self):
        response = self.client.get(TASKS_URL)

        tasks = Task.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(self.queryset),
            list(tasks)
        )
        self.assertTemplateUsed(
            response,
            "manager/task_list.html"
        )

    def test_pagination_is_ten(self):
        response = self.client.get(TASKS_URL)

        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["task_list"]), 6)


class TaskDetailTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="red")

        self.task_type = TaskType.objects.create(
            name="test778"
        )

        self.task = Task.objects.create(
            name="test12345",
            description="About task",
            deadline=now(),
            task_type=self.task_type
        )
        self.worker = get_user_model().objects.create_user(
            username="test",
            password="password123",
            position=self.position
        )

        self.another_worker = get_user_model().objects.create_user(
            username="worker",
            password="test123450",
            position=self.position
        )

        self.assignees = self.task.assignees.all()
        self.client.force_login(self.worker)

    def test_detail_task(self):
        response = self.client.get(
            reverse("manager:task-detail", kwargs={"pk": self.task.id})
        )

        self.assertTemplateUsed(
            response,
            "manager/task_detail.html"
        )

    def test_task_deadline(self):

        self.assertRaises(ValidationError, self.task.full_clean)
