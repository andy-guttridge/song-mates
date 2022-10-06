from . import views
from django.urls import path

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("user-delete/", views.UserDelete.as_view(), name="user_delete"),
]