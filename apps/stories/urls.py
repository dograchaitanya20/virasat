from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('', views.StoryListView.as_view(), name='list'),
    path('submit/', views.StorySubmitView.as_view(), name='submit'),
    path('<slug:slug>/', views.StoryDetailView.as_view(), name='detail'),
]
