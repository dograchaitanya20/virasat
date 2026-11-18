from django.contrib import admin
from .models import UserProfile, Bookmark

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'favorite_state', 'created_at')
    search_fields = ('user__username', 'user__email', 'location', 'favorite_state')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('user__username',)
