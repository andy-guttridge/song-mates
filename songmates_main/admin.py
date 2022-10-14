from django.contrib import admin
from .models import Profile, CollabRequest


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Specify fields to be accessible in the admin panel for the Profile model
    """
    prepopulated_fields = {'slug': ('user',)}
    raw_id_fields = ('friends'),
    list_display = ('user', 'slug', 'biog', 'genre1',
                    'instru_skill1')
    list_filter = ('user',)
    search_fields = ('user',)


@admin.register(CollabRequest)
class CollabRequestAdmin(admin.ModelAdmin):
    """
    Specify fields to be accessible in the admin panel for the CollabRequest model
    """
    list_display = ('from_user', 'to_user', 'date', 'message')
