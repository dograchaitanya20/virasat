import pytest
from apps.states.models import State
from apps.heritage.models import HeritageSite
from apps.festivals.models import Festival
from apps.arts.models import ArtForm
from apps.cuisine.models import CuisineDish
from apps.core.models import TimelineEvent
from apps.quiz.models import QuizQuestion, QuizScore
from apps.stories.models import Story
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_state_model():
    state = State.objects.create(
        name="Test Pradesh",
        capital="Test City",
        languages="Hindi, English",
        summary="A magnificent test state rich in heritage.",
        hero_image="https://example.com/test.jpg",
        lat=25.0,
        lng=80.0,
        region="North",
        famous_for="Test Monuments"
    )
    assert state.slug == "test-pradesh"
    assert str(state) == "Test Pradesh"
    assert state.get_absolute_url() == "/states/test-pradesh/"

@pytest.mark.django_db
def test_heritage_site_model():
    state = State.objects.create(
        name="Rajasthan Unique",
        capital="Jaipur",
        languages="Hindi",
        summary="Desert state",
        hero_image="https://example.com/test.jpg",
        lat=26.0,
        lng=75.0,
    )
    site = HeritageSite.objects.create(
        name="Hawa Mahal Palace",
        state=state,
        category="Fort",
        unesco=True,
        unesco_year=2019,
        era="Kachhwaha Dynasty (1799 CE)",
        description="Palace of winds with 953 jharokhas",
        history="Built by Maharaja Sawai Pratap Singh",
        visiting_info="Open 9 AM to 5 PM",
        lat=26.9239,
        lng=75.8267,
        hero_image="https://example.com/hawa.jpg"
    )
    assert site.slug == "hawa-mahal-palace"
    assert site.unesco is True
    assert "Hawa Mahal Palace" in str(site)
    assert site.get_absolute_url() == "/heritage/hawa-mahal-palace/"

@pytest.mark.django_db
def test_quiz_score_percentage_calculation():
    user = User.objects.create_user(username="testplayer", password="password123")
    score = QuizScore.objects.create(
        user=user,
        player_name="Test Player",
        score=8,
        total_questions=10,
        time_taken_seconds=45
    )
    assert score.percentage == 80.0
    assert "8/10 (80.0%)" in str(score)

@pytest.mark.django_db
def test_timeline_event_ordering():
    e1 = TimelineEvent.objects.create(
        year_era="c. 2600 BCE",
        year_numeric=-2600,
        title="Event Ancient",
        category="Ancient",
        description="Harappan city planning",
        hero_image="https://example.com/harappa.jpg"
    )
    e2 = TimelineEvent.objects.create(
        year_era="1950 CE",
        year_numeric=1950,
        title="Event Modern",
        category="Modern",
        description="Constitution adoption",
        hero_image="https://example.com/modern.jpg"
    )
    events = list(TimelineEvent.objects.all())
    assert events[0].year_numeric < events[1].year_numeric
