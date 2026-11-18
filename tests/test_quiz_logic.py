import pytest
import json
from django.urls import reverse
from apps.quiz.models import QuizQuestion, QuizScore

@pytest.mark.django_db
def test_quiz_play_view_context(client):
    QuizQuestion.objects.create(
        question="Which monument is known as the Symbol of Love?",
        option_a="Red Fort",
        option_b="Taj Mahal",
        option_c="Hampi",
        option_d="Qutub Minar",
        correct_option="B",
        explanation="Taj Mahal was built by Shah Jahan in memory of Mumtaz Mahal."
    )
    response = client.get(reverse('quiz:play'))
    assert response.status_code == 200
    assert 'questions_json' in response.context
    payload = json.loads(response.context['questions_json'])
    assert len(payload) >= 1
    assert payload[0]['correct_option'] == 'B'

@pytest.mark.django_db
def test_quiz_score_submission_and_leaderboard(client):
    payload = {
        'player_name': 'Chanakya Scholar',
        'score': 9,
        'total_questions': 10,
        'time_taken': 52
    }
    response = client.post(
        reverse('quiz:submit_score'),
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert 'rank' in data
    assert data['percentage'] == 90.0

    # Verify Leaderboard shows player
    res_leaderboard = client.get(reverse('quiz:leaderboard'))
    assert res_leaderboard.status_code == 200
    assert b'Chanakya Scholar' in res_leaderboard.content
