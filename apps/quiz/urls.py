from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.QuizPlayView.as_view(), name='play'),
    path('submit-score/', views.submit_score_api, name='submit_score'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
]
