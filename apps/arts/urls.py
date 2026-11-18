from django.urls import path
from . import views

app_name = 'arts'

urlpatterns = [
    path('', views.ArtListView.as_view(), name='list'),
    path('<slug:slug>/', views.ArtDetailView.as_view(), name='detail'),
]
