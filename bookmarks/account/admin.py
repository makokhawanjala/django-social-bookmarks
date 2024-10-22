from django.contrib import admin
from .models import Profile
@admin.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo', 'location']
    search_fields = ('user__username', 'location')
    list_filter = ('date_of_birth',)
    raw_id_fields = ['user']
    """This class customizes the admin interface for the Profile model.
    fieldsets = (
        (None, {
            'fields': ('user', 'bio', 'photo')
        }),
        ('Personal Info', {
            'fields': ('date_of_birth', 'location')
        }),
    )
    readonly_fields = ('user',)
    """
