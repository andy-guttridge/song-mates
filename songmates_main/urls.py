from . import views
from django.urls import path

urlpatterns = [
     path("", views.ProfileAccount.as_view(), name="home"),
     path("user-delete/", views.UserDelete.as_view(), name="user_delete"),
     path("update-profile/", views.UpdateProfile.as_view(),
          name="update_profile"),
     path("find-collabs/", views.FindCollabs.as_view(), name="find_collabs"),
     path("single-profile/<int:user_pk>", views.SingleProfile.as_view(),
          name="single_profile"),
     path("request-collab/<int:to_user_pk>", views.RequestCollab.as_view(),
          name="request_collab"),
     path("collab-requests/", views.CollabRequests.as_view(),
          name="collab_requests"),
     path("collab-requests/<int:user_pk>", views.CollabRequests.as_view(),
          name="collab_requests"),
]
