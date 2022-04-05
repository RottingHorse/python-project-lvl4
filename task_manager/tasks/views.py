"""Views for tasks with CRUD forms."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView
from task_manager.constants import BUTTON_TEXT, LOGIN, TITLE
from task_manager.tasks.constants import TASKS, TASKS_LIST
from task_manager.tasks.forms import TaskForm, TasksFilter
from task_manager.tasks.models import Task
from task_manager.tasks.translations import (
    BY_ITS_AUTHOR,
    CHANGE_TASK,
    CREATE_TASK,
    DELETE_TASK,
    SHOW_TITLE,
    TASK_CHANGED_SUCCESSFULLY,
    TASK_CREATED_SUCCESSFULLY,
    TASK_DELETED_SUCCESSFULLY,
    TASKS_TITLE,
)
from task_manager.translations import (
    CHANGE_TITLE,
    CREATE_TITLE,
    DELETE_BUTTON,
    NOT_AUTHORIZED,
)
from task_manager.users.models import User


class TasksListPage(LoginRequiredMixin, FilterView):
    """Tasks list page."""

    model = Task
    template_name = "tasks_list.html"
    context_object_name = TASKS
    filterset_class = TasksFilter

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

    def handle_no_permission(self):
        """Add error message and redirect to login page.

        Returns:
            Redirect to login page with message.
        """
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)


class CreateTaskPage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create task page."""

    model = Task
    form_class = TaskForm
    template_name = "form.html"
    success_url = reverse_lazy(TASKS_LIST)
    success_message = TASK_CREATED_SUCCESSFULLY

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

    def handle_no_permission(self):
        """Add error message and redirect to login page.

        Returns:
            Redirect to login page with message.
        """
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)


class ChangeTaskPage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change task page."""

    model = Task
    form_class = TaskForm
    template_name = "form.html"
    success_url = reverse_lazy(TASKS_LIST)
    success_message = TASK_CHANGED_SUCCESSFULLY

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

    def handle_no_permission(self):
        """Add ERROR message and redirect to login page.

        Returns:
            Redirect to login page with message.
        """
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)


class DeleteTaskPage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete task page."""

    model = Task
    template_name = "delete.html"
    success_url = reverse_lazy(TASKS_LIST)
    success_message = TASK_DELETED_SUCCESSFULLY

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

    def handle_no_permission(self):
        """Add error message and redirect to login page.

        Returns:
            Redirect to login page with message.
        """
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)
