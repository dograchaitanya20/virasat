from django.contrib import admin
from .models import TimelineEvent

@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('year_era', 'title', 'category', 'year_numeric', 'related_site')
    list_filter = ('category',)
    search_fields = ('title', 'year_era', 'description')
    ordering = ('year_numeric',)
    prepopulated_fields = {'slug': ('title',)}
