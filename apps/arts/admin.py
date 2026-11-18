from django.contrib import admin
from .models import ArtForm

@admin.register(ArtForm)
class ArtFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'origin_state', 'unesco_intangible')
    list_filter = ('category', 'unesco_intangible', 'origin_state')
    search_fields = ('name', 'history', 'description', 'famous_practitioners')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('unesco_intangible',)
