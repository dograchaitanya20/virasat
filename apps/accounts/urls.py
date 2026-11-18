from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='core:home'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('bookmarks/', views.BookmarksView.as_view(), name='bookmarks'),
    path('toggle-bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
]
