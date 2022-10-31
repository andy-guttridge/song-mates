from . import views
from django.urls import path

urlpatterns = [
    path("", views.FindCollabs.as_view(), name="home"),
    path("edit-profile/", views.ProfileAccount.as_view(), name="edit_profile"),
    path("user-delete/", views.UserDelete.as_view(), name="user_delete"),
    path("update-profile/", views.UpdateProfile.as_view(),
         name="update_profile"),
    path("single-profile/<int:user_pk>", views.SingleProfile.as_view(),
         name="single_profile"),
    path("request-collab/<int:to_user_pk>", views.RequestCollab.as_view(),
         name="request_collab"),
    path("collab-requests/", views.CollabRequests.as_view(),
         name="collab_requests"),
    path("collab-requests/<int:user_pk>", views.CollabRequests.as_view(),
         name="collab_requests"),
    path("delete-collab/<int:user_pk>", views.DeleteCollab.as_view(),
         name="delete_collab"),
    path("search-profile/", views.SearchProfile.as_view(),
         name="search_profile"),
    path("send-msg/<int:to_user_pk>", views.SendMsg.as_view(),
         name="send_msg"),
    path("messages/", views.Messages.as_view(),
         name="messages"),
]
