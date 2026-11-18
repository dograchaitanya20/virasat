from django.contrib import admin
from .models import Festival

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ('name', 'month', 'approximate_dates', 'religion_or_type', 'is_featured')
    list_filter = ('month', 'religion_or_type', 'is_featured')
    search_fields = ('name', 'significance', 'rituals', 'food')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('states',)
    list_editable = ('is_featured',)
