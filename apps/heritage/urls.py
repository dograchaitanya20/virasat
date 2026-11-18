from django.urls import path
from . import views

app_name = 'heritage'

urlpatterns = [
    path('', views.HeritageListView.as_view(), name='list'),
    path('<slug:slug>/', views.HeritageDetailView.as_view(), name='detail'),
]
