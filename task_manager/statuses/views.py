"""Views for statuses with CRUD forms."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..mixins import HandleNoPermissionMixin
from .constants import BUTTON_TEXT, LOGIN, STATUSES, STATUSES_LIST, TITLE
from .forms import StatusForm
from .models import Status
from .translations import (
    CHANGE_STATUS,
    CHANGE_TITLE,
    CREATE_STATUS,
    CREATE_TITLE,
    DELETE_BUTTON,
    DELETE_STATUS,
    NOT_AUTHORIZED,
    STATUS_CHANGED_SUCCESSFULLY,
    STATUS_CREATED_SUCCESSFULLY,
    STATUS_DELETED_SUCCESSFULLY,
    STATUS_IN_USE,
    STATUSES_TITLE,
)


class StatusesListPage(
    LoginRequiredMixin,
    HandleNoPermissionMixin,
    ListView,
):
    """Statuses list page."""

    model = Status
    template_name = "statuses_list.html"
    context_object_name = STATUSES
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

    def get_context_data(self, **kwargs):
        """Add title text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = STATUSES_TITLE
        return context


class CreateStatusPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    CreateView,
):
    """Create status page."""

    model = Status
    form_class = StatusForm
    template_name = "form.html"
    success_url = reverse_lazy(STATUSES_LIST)
    success_message = STATUS_CREATED_SUCCESSFULLY
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
        context[TITLE] = CREATE_STATUS
        context[BUTTON_TEXT] = CREATE_TITLE
        return context


class ChangeStatusPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    UpdateView,
):
    """Change status page."""

    model = Status
    form_class = StatusForm
    template_name = "form.html"
    success_url = reverse_lazy(STATUSES_LIST)
    success_message = STATUS_CHANGED_SUCCESSFULLY
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
        context[TITLE] = CHANGE_STATUS
        context[BUTTON_TEXT] = CHANGE_TITLE
        return context


class DeleteStatusPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    DeleteView,
):
    """Delete status page."""

    model = Status
    template_name = "delete.html"
    success_url = reverse_lazy(STATUSES_LIST)
    success_message = STATUS_DELETED_SUCCESSFULLY
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

    def form_valid(self, form):
        """Check if status has tasks.

        Args:
            form: Status delete form.

        Returns:
            Redirect to statuses with error message or HttpResponse.
        """
        if self.get_object().tasks.all():
            messages.error(self.request, STATUS_IN_USE)
        else:
            super(DeleteStatusPage, self).form_valid(form)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        """Add title and button text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = DELETE_STATUS
        context[BUTTON_TEXT] = DELETE_BUTTON
        return context
