from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.db.models import Q
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
        profile_queryset = Profile.objects.filter(user=request.user)
        get_object_or_404(profile_queryset)
        profile = profile_queryset.first()
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

        profile_queryset = Profile.objects.filter(user=request.user)
        get_object_or_404(profile_queryset)
        profile = profile_queryset.first()
        profile_form = ProfileForm(request.POST, request.FILES,
                                   instance=profile)
        # Check if user hit submit button and form is valid. Save if true.
        # Otherwise reload page using existing data
        if profile_form.is_valid() and 'profile-form-submit' in request.POST:
            profile_form.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
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
    Retrieve user profiles from data base and pass to the find_collabs
    template.
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # Find all profiles and any pending collaboration requests
        # sent by or to the user
        profiles = Profile.objects.order_by('user')
        collab_requests_from_user = CollabRequest.objects.filter(
                from_user=request.user
            )
        collab_requests_to_user = CollabRequest.objects.filter(
                to_user=request.user
            )
        collaborators = Profile.objects.filter(user=request.user).first().\
            friends.all()
    
        # Pull the to_users out of any collaboration requests sent by or
        # to this user and add to a list
        collab_request_users = []
        for collab_request in collab_requests_from_user:
            collab_request_users.append(collab_request.to_user)
        for collab_request in collab_requests_to_user:
            collab_request_users.append(collab_request.from_user)
        return render(
            request,
            "find_collabs.html",
            {
                "profiles": profiles,
                "collab_request_users": collab_request_users,
                "collaborators": collaborators,
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


class CollabRequests(View):
    """
    View of the user's currently pending collaboration requests.
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # Get all pending incoming and outgoing collaboration requests
        in_requests = CollabRequest.objects.filter(to_user=request.user)
        out_requests = CollabRequest.objects.filter(from_user=request.user)
        return render(
            request,
            "collab_requests.html",
            {
                "in_requests": in_requests,
                "out_requests": out_requests,
            }
        )
    
    @method_decorator(login_required)
    def post(self, request, user_pk, *args, **kwargs):
        # If the user has pressed the approve request button, find the user's
        # profile, the new friend's profile and add to the many-to-many list of
        # friends for both users.
        if 'collab-approve' in request.POST:
            profile = Profile.objects.filter(user=request.user).first()
            new_friend = Profile.objects.filter(user=user_pk).first()
            if new_friend:
                profile.friends.add(new_friend)
                profile.save()
        
        # Find the right collaboration request depending if this was an
        # incoming or outgoing request, and delete - regardless of whether
        # it was an approval, rejection or cancellation.
        if 'collab-approve' in request.POST or 'collab-reject' in request.POST:
            collab_request = CollabRequest.objects.filter(
                from_user=user_pk
                ).first()
        elif 'collab-cancel' in request.POST:
            collab_request = CollabRequest.objects.filter(
                to_user=user_pk
                ).first()

        if collab_request:
            collab_request.delete()        
        
        # Re-render the page
        in_requests = CollabRequest.objects.filter(to_user=request.user)
        out_requests = CollabRequest.objects.filter(from_user=request.user)
        return render(
            request,
            "collab_requests.html",
            {
                "in_requests": in_requests,
                "out_requests": out_requests,
            }
        )


class SingleProfile(View):
    """
    Displays a single user profile.
    """
    def get(self, request, user_pk, *args, **kwargs):
        # Find the profile we need to display and retrieve any collaboration
        # request involving both the authenticated user and the user whose
        # profile we need to display. Then render the profile.
        profile_queryset = Profile.objects.filter(user=user_pk)
        get_object_or_404(profile_queryset)
        profile = profile_queryset.first()
        collab_request_queryset = CollabRequest.objects.filter(
            Q(from_user=profile.user) | Q(to_user=profile.user)
            )
        collab_request = collab_request_queryset.first()
        if profile.friends.filter(user=request.user):
            is_collaborator = True
        else:
            is_collaborator = False
        return render(
            request,
            "single_profile.html",
            {
                "profile": profile,
                "collab_request": collab_request,
                "is_collaborator": is_collaborator,
            }
        )


class DeleteCollab(View):
    """
    Deletes collaboration connection between two users
    """
    def post(self, request, user_pk, *args, **kwards):
        # Find the collaborator's profile
        collaborator_queryset = Profile.objects.filter(user=user_pk)
        get_object_or_404(collaborator_queryset)
        collaborator_profile = collaborator_queryset.first()

        # Find the authenticated user's profile
        user_queryset = Profile.objects.filter(user=request.user)
        get_object_or_404(user_queryset)
        user_profile = user_queryset.first()

        # Check both profiles exist and remove the many to many relationship
        # between them on each side.
        if user_profile.friends.filter(pk=collaborator_profile.pk).exists():
            user_profile.friends.remove(collaborator_profile)
        if collaborator_profile.friends.filter(pk=user_profile.pk).exists():
            collaborator_profile.friends.remove(user_profile)
        return HttpResponseRedirect(reverse_lazy('find_collabs'))
