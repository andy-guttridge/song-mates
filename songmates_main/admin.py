from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('user',)}
    raw_id_fields = ('friends'),
    list_display = ('user', 'slug', 'biog', 'genre1',
                    'instru_skill1')
    list_filter = ('user',)
    search_fields = ('user',)
