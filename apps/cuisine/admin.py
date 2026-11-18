from django.contrib import admin
from .models import CuisineDish

@admin.register(CuisineDish)
class CuisineDishAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'veg_or_non_veg', 'meal_type', 'spice_level')
    list_filter = ('veg_or_non_veg', 'meal_type', 'spice_level', 'state')
    search_fields = ('name', 'ingredients', 'story')
    prepopulated_fields = {'slug': ('name',)}
