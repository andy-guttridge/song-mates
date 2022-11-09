from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.db.models import Q, F
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.decorators import method_decorator
from cloudinary.exceptions import Error
from .models import Profile, CollabRequest, Message
from .forms import ProfileForm, SearchForm
from .functions import find_collabs


class Home(View):
    """
    The site homepage
    """
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "home.html"
        )


class ProfileAccount(View):
    """
    User profile and account view.
    Redirects to login page if user not authenticated.
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # If a profile for this user does not exist, create one
        if not Profile.objects.filter(user=request.user).exists():
            profile = Profile(user=request.user)
            profile.save()
        # Retrieve profile from database, create form from it and
        # render
        profile_queryset = Profile.objects.filter(user=request.user)
        get_object_or_404(profile_queryset)
        profile = profile_queryset.first()
        profile_form = ProfileForm(instance=profile)
        return render(
            request,
            "edit_profile.html",
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
            profile_form.clean()
            try:
                profile_form.save()
            except Error:
                messages.error(request, "Error in form submission. Did you\
                                try to upload a file that isn't an image?")
            return HttpResponseRedirect(reverse_lazy('edit_profile'))
        else:
            profile_form = ProfileForm(instance=profile)
            return HttpResponseRedirect(reverse_lazy('edit_profile'))


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
    def get(self, request, *args, **kwargs):
        # Find all profiles, any pending collab requests
        # and current collabs
        profiles = Profile.objects.order_by('user__username')

        # Find any collabs and collab requests if user is authenticated
        # and divert them to edit profile if they don't yet have a profile
        if request.user.is_authenticated:
            user_profile = Profile.objects.filter(user=request.user).first()
            if user_profile is None:
                return HttpResponseRedirect(reverse_lazy('edit_profile'))
            collab_request_users = find_collabs(request.user)
            collaborators = Profile.objects.filter(user=request.user).first().\
                friends.all()
        

        
        # Create instance of the search form
        search_form = SearchForm(is_authenticated=request.user.is_authenticated)
        if request.user.is_authenticated:
            return render(
                request,
                "find_collabs.html",
                {
                    "profiles": profiles,
                    "user_profile": user_profile,
                    "collab_request_users": collab_request_users,
                    "collaborators": collaborators,
                    "user": request.user,
                    "search_form": search_form
                },
            )
        else:
            return render(
                request,
                "find_collabs.html",
                {
                    "profiles": profiles,
                    "search_form": search_form
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
    @method_decorator(login_required)
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
    @method_decorator(login_required)
    def post(self, request, user_pk, *args, **kwargs):
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


class SearchProfile(View):
    """
    Handle search form submission
    """
    def get(self, request, *args, **kwargs):
        # Clear search and form if 'Show all' button pressed
        if 'search-form-show-all' in request.GET:
            return HttpResponseRedirect(reverse_lazy('find_collabs'))
        
        # Retrieve only profiles of approved collaborators if
        # collabs_only checkbox selected, otherwise retrieve all
        # profiles
        collabs_only = request.GET.get('collabs_only')
        if collabs_only == 'on':
            profiles_queryset = Profile.objects.filter(user=request.user).\
                first().friends.order_by('user__username')
        else:
            profiles_queryset = Profile.objects.order_by('user__username')
        
        # Retrieve any genres selected and search phrase entered
        # Using the getlist method to access a list returned by a multiple
        # choice form element is from
        # https://stackoverflow.com/questions/21666963/django-forms-multiplechoicefield-only-selects-one-value
        genres = request.GET.getlist('genres')
        search_phrase = request.GET.get('search_phrase')
        username = request.user.username

        # Find current collabs and pending collab requests
        if request.user.is_authenticated:
            collaborators = Profile.objects.filter(user=request.user).first().\
                friends.all()
            collab_request_users = find_collabs(request.user)
        
        # Retrieve profiles that match any selected genres.
        # Technique of using _in to check if the value of a field exists
        # within a list from
        # https://stackoverflow.com/questions/70703168/check-if-each-value-within-list-is-present-in-the-given-django-model-table-in-a
        genres_profiles_queryset = Profile.objects.filter(
            Q(genre1__in=genres) |
            Q(genre2__in=genres) |
            Q(genre3__in=genres) |
            Q(genre4__in=genres) |
            Q(genre5__in=genres)
            )
        
        # Retrieve profiles that match search phrase
        search_phrase_profiles_queryset = Profile.objects.filter(
            # How to search on the property of a foreign key object from
            # https://stackoverflow.com/questions/35012942/related-field-got-invalid-lookup-icontains
            Q(user__username__icontains=search_phrase) |
            Q(biog__search=search_phrase) |
            Q(instru_skill1__icontains=search_phrase) |
            Q(instru_skill2__icontains=search_phrase) |
            Q(instru_skill3__icontains=search_phrase) |
            Q(instru_skill4__icontains=search_phrase) |
            Q(instru_skill5__icontains=search_phrase)
        )
        
        # Retrieve profiles that match genres and search phrase...
        if genres_profiles_queryset and search_phrase_profiles_queryset:
            final_search_queryset = search_phrase_profiles_queryset\
                .intersection(genres_profiles_queryset)
        # Or just matches to genre or search phrase if user only searched one
        # of these
        else:
            final_search_queryset = search_phrase_profiles_queryset.union(
                genres_profiles_queryset
                )
        # Retrieve profiles matched by search and those that are approved
        # collabs if user had selected collabs_only
        final_queryset = final_search_queryset.intersection(profiles_queryset)
        
        # If collabs_only selected and no other search requested,
        # return all approved collabs, otherwise return final queryset
        if collabs_only == 'on' and final_queryset is None:
            final_profiles = profiles_queryset.all()
        else:
            final_profiles = sorted(list(final_queryset.all()),
                                    key=lambda profile: profile.user.username)
        
        # Technique of using initial argument to set value of form input from
        # https://stackoverflow.com/questions/604266/django-set-default-form-values
        search_form = SearchForm(initial={
                'collabs_only': collabs_only,
                'genres': genres,
                'search_phrase': search_phrase
            },
                is_authenticated=request.user.is_authenticated
            )

        if request.user.is_authenticated:
            user_profile = Profile.objects.filter(user=request.user).\
                first()
            return render(
                request,
                "find_collabs.html",
                {
                    "profiles": final_profiles,
                    "user_profile": user_profile,
                    "collab_request_users": collab_request_users,
                    "collaborators": collaborators,
                    "user": request.user,
                    "search_form": search_form
                }
            )
        else:
            return render(
                request,
                "find_collabs.html",
                {
                    "profiles": final_profiles,
                    "search_form": search_form
                }
            )


class SendMsg(View):
    """
    Deal with user's request to send a message to another user.
    """
    @method_decorator(login_required)
    def post(self, request, to_user_pk, *args, **kwargs):

        # Check if user is still a collaborator
        is_collaborator = False
        if Profile.objects.filter(user=to_user_pk).exists():
            profile_queryset = Profile.objects.filter(user=to_user_pk)
            profile = profile_queryset.first()
            if profile.friends.filter(user=request.user):
                is_collaborator = True
        else:
            profile = None

        # Check if the user they want to message exists
        # and is a collaborator - if so send message
        if User.objects.filter(pk=to_user_pk).exists() and is_collaborator:
            to_user = User.objects.filter(pk=to_user_pk).first()
            subject = request.POST.get('msg-subject')
            message = request.POST.get('msg-body')
            # Create a new message and save
            message = Message(from_user=request.user, to_user=to_user,
                              subject=subject, message=message)
            message.save()

        # If the user and profile exists but isn't a collaborator, inform the
        # sender and don't send the message
        elif profile and not is_collaborator:
            messages.info(
                request,
                'The user you have attempted to '
                'message is not your collaborator.'
            )
        
        # If the profile doesn't exist, inform the sender and don't send the
        # message
        else:
            messages.info(
                request,
                'The user you have attempted to '
                'message has deleted their profile.'
            )

        # Return to messages view if that's where the sent message came from,
        # otherwise back to find_collabs.
        if 'reply-msg' in request.POST:
            return HttpResponseRedirect(reverse_lazy('messages'))
        else: 
            return HttpResponseRedirect(reverse_lazy('find_collabs'))


class Messages(View):
    """
    View of the user's messages inbox and outbox.
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # Get all messages in inbox and outbox
        in_messages = Message.objects.filter(to_user=request.user).order_by('date')
        out_messages = Message.objects.filter(from_user=request.user).order_by('date')
        return render(
            request,
            "messages.html",
            {
                "in_messages": in_messages,
                "out_messages": out_messages,
            }
        )


class DeleteMsg(View):
    """
    Handle request to delete a user message
    """
    @method_decorator(login_required)
    def post(self, request, message_pk, *args, **kwargs):
        # Find the message to be deleted
        message_queryset = Message.objects.filter(pk=message_pk)
        get_object_or_404(message_queryset)
        message = message_queryset.first()

        # Find the authenticated user's profile
        user_queryset = Profile.objects.filter(user=request.user)
        get_object_or_404(user_queryset)
        user_profile = user_queryset.first()

        # Check if the request to delete the message was for an incoming
        # or outgoing message, check the request came from the actual user who
        # received or sent the message. If so, mark it as deletable on their
        # side of the message
        if ('confirm-msg-in-delete' in request.POST
                and user_profile.user == message.to_user):
            message.to_deleted = True
            message.save()
        if ('confirm-msg-out-delete' in request.POST
                and user_profile.user == message.from_user):
            message.from_deleted = True
            message.save()
        
        # If message has been marked as deletable by both sending and receiving
        # users, delete it
        message_queryset = Message.objects.filter(pk=message_pk)
        get_object_or_404(message_queryset)
        if message.from_deleted is True and message.to_deleted is True:
            message.delete()
            
        return HttpResponseRedirect(reverse_lazy('messages'))


class PageNotFoundError(View):
    def get(request, *args, **kwargs):
        return render(request, '404.html')


class ServerError(View):
    def get(request, *args, **kwargs):
        return render(request, '500.html')
