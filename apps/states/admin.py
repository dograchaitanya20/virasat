from django.contrib import admin
from .models import State

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'capital', 'region', 'languages', 'best_time_to_visit')
    list_filter = ('region',)
    search_fields = ('name', 'capital', 'languages', 'famous_for')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
