from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from .models import Profile, CollabRequest
from .forms import ProfileForm


class ProfileAccount(View):
    """
    User profile and account view.
    Redirects to login page if user not authenticated.
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # If a profile for this user does not exist, create one
        if not Profile.objects.filter(user=request.user).exists():
            profile = Profile(user=request.user, slug=request.user.id)
            profile.save()
        # Retrieve profile from database, create form from it and
        # render
        profile = Profile.objects.filter(user=request.user).first()
        profile_form = ProfileForm(instance=profile)
        return render(
            request,
            "index.html",
            {
                "profile": profile,
                "form": profile_form
            }
        )


class UpdateProfile(View):
    """
    Handle updates to user profile.
    Redirects to login page if user not authenticated.
    """
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # Find user profile in database, associate with form
        # and populate form using POST request data
        profile = Profile.objects.filter(user=request.user).first()
        profile_form = ProfileForm(request.POST, request.FILES,
                                   instance=profile)
        # Check if user hit submit button and form is valid. Save if true.
        # Otherwise reload page using existing data
        if profile_form.is_valid() and 'profile-form-submit' in request.POST:
            profile_form.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            profile = Profile.objects.filter(user=request.user).first()
            profile_form = ProfileForm(instance=profile)
            return HttpResponseRedirect(reverse_lazy('home'))


class UserDelete(View):
    """
    Make user account inactive if user confirms delete action.
    """
    # Approach to making a user account inactive adapated from
    # https://stackoverflow.com/questions/38047408/how-to-allow-user-to-delete-account-in-django-allauth
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # Check there is a profile for the user and delete if so
        if Profile.objects.filter(user=request.user).exists():
            profile = Profile.objects.filter(user=request.user)
            profile.delete()
        # Make user account inactive
        request.user.is_active = False
        request.user.save()
        return HttpResponseRedirect(reverse_lazy('account_logout'))


class FindCollabs(View):
    """
    Retrieve user profiles from data base and pass to the find_collabs template.
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # Find all profiles and any pending collaboration requests
        # sent by the user
        profiles = Profile.objects.order_by('user')
        collab_requests = CollabRequest.objects.filter(from_user=request.user)
        collab_request_users = []

        # Pull the to_users out of any collaboration requests sent by this user
        # and add to a list
        for collab_request in collab_requests:
            collab_request_users.append(collab_request.to_user)
        return render(
            request,
            "find_collabs.html",
            {
                "profiles": profiles,
                "collab_request_users": collab_request_users,
                "user": request.user
            }
        )


class RequestCollab(View):
    """
    Deal with user's request to send a collaboration request to another user.
    """
    @method_decorator(login_required)
    def post(self, request, to_user_pk, *args, **kwargs):
        # Check if the user they want to collab with exists
        # and retrieve if it does

        if User.objects.filter(pk=to_user_pk).exists():
            to_user = User.objects.filter(pk=to_user_pk).first()

        # Create a new collaboration request and save
        collab_request = CollabRequest(from_user=request.user, to_user=to_user)
        collab_request.save()
        return HttpResponseRedirect(reverse_lazy('find_collabs'))