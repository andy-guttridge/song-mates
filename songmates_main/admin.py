from django.contrib import admin
from .models import Profile, CollabRequest


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Specify fields to be accessible in the admin panel for the Profile model
    """
    raw_id_fields = ('friends'),
    list_display = ('user', 'get_profile_complete', 'biog', 'get_collaborators')
    list_filter = ('user',)
    search_fields = ('user',)

    def get_collaborators(self, obj):
        """
        Create a string of the user's approved collaborators
        """
        # Approach to creating a string representation of a many-to-many field adapted from
        # https://stackoverflow.com/questions/18108521/many-to-many-in-list-display-django
        string = ""
        for friend in obj.friends.all():
            string += str(friend.user) + ', '
        return string
    
    def get_profile_complete(self, obj):
        """
        Return a string representation of the profile_complete field
        """
        return 'True' if obj.profile_complete is True else 'False'
        


@admin.register(CollabRequest)
class CollabRequestAdmin(admin.ModelAdmin):
    """
    Specify fields to be accessible in the admin panel for the CollabRequest model
    """
    list_display = ('from_user', 'to_user', 'date', 'message')
