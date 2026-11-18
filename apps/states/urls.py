from django.urls import path
from . import views

app_name = 'states'

urlpatterns = [
    path('', views.StateListView.as_view(), name='list'),
    path('<slug:slug>/', views.StateDetailView.as_view(), name='detail'),
    path('<slug:slug>/panel/', views.state_panel_partial, name='panel_partial'),
]
