"""
URL Configuration for Virasat (विरासत)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#D4AF37"><path d="M12 2C12 2 9 6.5 9 10C9 11.66 10.34 13 12 13C13.66 13 15 11.66 15 10C15 6.5 12 2 12 2ZM5.5 8C4.12 8 3 9.12 3 10.5C3 13.5 7.5 16.5 7.5 16.5C7.5 16.5 6.5 14.5 6.5 13C6.5 11.9 7.4 11 8.5 11C8.85 11 9.18 11.09 9.47 11.26C8.57 10.3 8 9 8 8C8 8 6.5 8 5.5 8ZM18.5 8C17.5 8 16 8 16 8C16 9 15.43 10.3 14.53 11.26C14.82 11.09 15.15 11 15.5 11C16.6 11 17.5 11.9 17.5 13C17.5 14.5 16.5 16.5 16.5 16.5C16.5 16.5 21 13.5 21 10.5C21 9.12 19.88 8 18.5 8ZM12 14C9.5 14 4 15.5 4 19V21H20V19C20 15.5 14.5 14 12 14Z"/></svg>"""

def favicon_view(request):
    return HttpResponse(FAVICON_SVG, content_type="image/svg+xml")

from apps.core.sitemaps import (
    StaticViewSitemap,
    HeritageSiteSitemap,
    FestivalSitemap,
    ArtFormSitemap,
    CuisineSitemap,
    StateSitemap,
    StorySitemap
)

sitemaps = {
    'static': StaticViewSitemap,
    'heritage': HeritageSiteSitemap,
    'festivals': FestivalSitemap,
    'arts': ArtFormSitemap,
    'cuisine': CuisineSitemap,
    'states': StateSitemap,
    'stories': StorySitemap,
}

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('favicon.ico', favicon_view, name='favicon'),
    
    # App URLs
    path('', include('apps.core.urls')),
    path('heritage/', include('apps.heritage.urls')),
    path('festivals/', include('apps.festivals.urls')),
    path('arts/', include('apps.arts.urls')),
    path('cuisine/', include('apps.cuisine.urls')),
    path('states/', include('apps.states.urls')),
    path('stories/', include('apps.stories.urls')),
    path('quiz/', include('apps.quiz.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('api/', include('apps.core.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'apps.core.views.custom_404'
handler500 = 'apps.core.views.custom_500'
