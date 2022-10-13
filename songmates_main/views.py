from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Profile
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
            print(profile.pk)
        # Retrieve profile from database, create form from it and
        # render
        profile = Profile.objects.filter(user=request.user).first()
        profile_form = ProfileForm(instance=profile)
        return render(
            request,
            "index.html",
            {
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
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "find_collabs.html",
        )
