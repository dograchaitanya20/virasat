from django.urls import path
from . import views

app_name = 'cuisine'

urlpatterns = [
    path('', views.CuisineListView.as_view(), name='list'),
    path('<slug:slug>/', views.CuisineDetailView.as_view(), name='detail'),
]
