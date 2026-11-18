from django.contrib import admin
from .models import HeritageSite, HeritageSiteImage

class HeritageSiteImageInline(admin.TabularInline):
    model = HeritageSiteImage
    extra = 2

@admin.register(HeritageSite)
class HeritageSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'category', 'unesco', 'built_year', 'era')
    list_filter = ('category', 'unesco', 'state__region', 'state')
    search_fields = ('name', 'description', 'history', 'architecture_style', 'built_by')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [HeritageSiteImageInline]
    list_editable = ('unesco',)
