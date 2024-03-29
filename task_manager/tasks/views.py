"""Views for tasks with CRUD forms."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from ..mixins import HandleNoPermissionMixin
from ..users.models import User
from .constants import (
    BUTTON_TEXT,
    LABELS,
    LOGIN,
    TASK,
    TASKS,
    TASKS_LIST,
    TITLE,
)
from .forms import TaskForm, TasksFilter
from .models import Task
from .translations import (
    BY_ITS_AUTHOR,
    CHANGE_TASK,
    CHANGE_TITLE,
    CREATE_TASK,
    CREATE_TITLE,
    DELETE_BUTTON,
    DELETE_TASK,
    NOT_AUTHORIZED,
    SHOW_TITLE,
    TASK_CHANGED_SUCCESSFULLY,
    TASK_CREATED_SUCCESSFULLY,
    TASK_DELETED_SUCCESSFULLY,
    TASK_VIEW,
    TASKS_TITLE,
)


class TasksListPage(
    LoginRequiredMixin,
    HandleNoPermissionMixin,
    FilterView,
):
    """Tasks list page."""

    model = Task
    template_name = "tasks_list.html"
    context_object_name = TASKS
    filterset_class = TasksFilter
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

    def get_context_data(self, **kwargs):
        """Add title and button text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = TASKS_TITLE
        context[BUTTON_TEXT] = SHOW_TITLE
        return context


class CreateTaskPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    CreateView,
):
    """Create task page."""

    model = Task
    form_class = TaskForm
    template_name = "form.html"
    success_url = reverse_lazy(TASKS_LIST)
    success_message = TASK_CREATED_SUCCESSFULLY
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

    def form_valid(self, form):
        """Add current user as task author.

        Args:
            form: Task create form.

        Returns:
            HttpResponse.
        """
        form.instance.author = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add title and button text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = CREATE_TASK
        context[BUTTON_TEXT] = CREATE_TITLE
        return context


class ChangeTaskPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    UpdateView,
):
    """Change task page."""

    model = Task
    form_class = TaskForm
    template_name = "form.html"
    success_url = reverse_lazy(TASKS_LIST)
    success_message = TASK_CHANGED_SUCCESSFULLY
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

    def get_context_data(self, **kwargs):
        """Add title and button text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = CHANGE_TASK
        context[BUTTON_TEXT] = CHANGE_TITLE
        return context


class DeleteTaskPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    DeleteView,
):
    """Delete task page."""

    model = Task
    template_name = "delete.html"
    success_url = reverse_lazy(TASKS_LIST)
    success_message = TASK_DELETED_SUCCESSFULLY
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

    def form_valid(self, form):
        """Check if user is author.

        Args:
            form: Task delete form.

        Returns:
            Redirect to tasks with error message or HttpResponse.
        """
        if self.request.user == self.get_object().author:
            super(DeleteTaskPage, self).form_valid(form)
        else:
            messages.error(self.request, BY_ITS_AUTHOR)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        """Add title and button text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = DELETE_TASK
        context[BUTTON_TEXT] = DELETE_BUTTON
        return context


class TaskDetailPage(
    LoginRequiredMixin,
    HandleNoPermissionMixin,
    DetailView,
):
    """Task details page."""

    model = Task
    template_name = "task_details.html"
    context_object_name = TASK
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

    def get_context_data(self, **kwargs):
        """Add title and labels list to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super(TaskDetailPage, self).get_context_data()
        context[TITLE] = TASK_VIEW
        context[LABELS] = self.get_object().labels.all()
        return context
