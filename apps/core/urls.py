from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('map/', views.MapView.as_view(), name='map'),
    path('timeline/', views.TimelineView.as_view(), name='timeline'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('search/', views.quick_search, name='quick_search'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
]
