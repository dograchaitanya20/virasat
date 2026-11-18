from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    path('stats/', api_views.stats_api, name='stats'),
    path('states/', api_views.StateListAPI.as_view(), name='states_list'),
    path('heritage/', api_views.HeritageListAPI.as_view(), name='heritage_list'),
    path('festivals/', api_views.FestivalListAPI.as_view(), name='festivals_list'),
    path('arts/', api_views.ArtListAPI.as_view(), name='arts_list'),
    path('cuisine/', api_views.CuisineListAPI.as_view(), name='cuisine_list'),
    path('timeline/', api_views.TimelineListAPI.as_view(), name='timeline_list'),
]
