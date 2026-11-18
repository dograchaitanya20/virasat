from django.contrib import admin
from .models import Story

@admin.action(description="Publish selected stories to Living Archives")
def make_published(modeladmin, request, queryset):
    queryset.update(status='published')

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'views_count')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'excerpt', 'body', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_published]
    list_editable = ('status',)
