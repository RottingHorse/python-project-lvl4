"""General urls."""
from django.contrib import admin
from django.urls import include, path

from .constants import (
    ADMIN_URL,
    INDEX,
    LABELS_URL,
    LOGIN,
    LOGIN_URL,
    LOGOUT,
    LOGOUT_URL,
    STATUSES_URL,
    TASKS_URL,
    USERS_URL,
)
from .views import IndexPage, LoginPage, LogoutPage

urlpatterns = [
    path("", IndexPage.as_view(), name=INDEX),
    path(LOGIN_URL, LoginPage.as_view(), name=LOGIN),
    path(LOGOUT_URL, LogoutPage.as_view(), name=LOGOUT),
    path(USERS_URL, include("task_manager.users.urls")),
    path(STATUSES_URL, include("task_manager.statuses.urls")),
    path(TASKS_URL, include("task_manager.tasks.urls")),
    path(LABELS_URL, include("task_manager.labels.urls")),
    path(ADMIN_URL, admin.site.urls),
]
