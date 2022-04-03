from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.constants import (
    STATUSES_DELETE,
    STATUSES_CHANGE,
    STATUSES_CREATE,
    STATUSES_LIST,
    STATUS_CREATED_SUCCESSFULLY,
    STATUS_CHANGED_SUCCESSFULLY,
    STATUS_IN_USE,
    STATUS_DELETED_SUCCESSFULLY,
    STATUSES,
    NAME,
    STATUSES_TEST,
    LOGIN_TEST,
)


class TestStatuses(TestCase):
    fixtures = ["statuses.json", "users.json", "tasks.json", "labels.json"]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.task1 = Task.objects.get(pk=1)

        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)

    def test_statuses_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(STATUSES_LIST))
        self.assertEqual(response.status_code, 200)
        statuses_list = list(response.context[STATUSES])
        self.assertQuerysetEqual(statuses_list, [self.status1, self.status2])

    def test_statuses_list_no_login(self):
        response = self.client.get(reverse(STATUSES_LIST))
        self.assertRedirects(response, LOGIN_TEST)

    def test_create_status(self):
        self.client.force_login(self.user)
        status = {NAME: "status3"}
        response = self.client.post(reverse(STATUSES_CREATE), status, follow=True)
        self.assertRedirects(response, STATUSES_TEST)
        self.assertContains(response, _(STATUS_CREATED_SUCCESSFULLY))
        created_status = Status.objects.get(name=status[NAME])
        self.assertEquals(created_status.name, "status3")

    def test_change_status(self):
        self.client.force_login(self.user)
        url = reverse(STATUSES_CHANGE, args=(self.status1.pk,))
        new_status = {NAME: "status4"}
        response = self.client.post(url, new_status, follow=True)
        self.assertRedirects(response, STATUSES_TEST)
        self.assertContains(response, _(STATUS_CHANGED_SUCCESSFULLY))
        self.assertEqual(Status.objects.get(pk=self.status1.id), self.status1)

    def test_status_with_tasks_delete(self):
        self.client.force_login(self.user)
        url = reverse(STATUSES_DELETE, args=(self.status1.pk,))
        response = self.client.post(url, follow=True)
        self.assertTrue(Status.objects.filter(pk=self.status1.id).exists())
        self.assertRedirects(response, STATUSES_TEST)
        self.assertContains(response, _(STATUS_IN_USE))

    def test_delete_status(self):
        self.client.force_login(self.user)
        self.task1.delete()
        url = reverse(STATUSES_DELETE, args=(self.status1.pk,))
        response = self.client.post(url, follow=True)
        # noinspection PyTypeChecker
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(pk=self.status1.pk)
        self.assertRedirects(response, STATUSES_TEST)
        self.assertContains(response, _(STATUS_DELETED_SUCCESSFULLY))
