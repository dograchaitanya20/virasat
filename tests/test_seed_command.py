import pytest
from django.core.management import call_command
from apps.states.models import State
from apps.heritage.models import HeritageSite
from apps.festivals.models import Festival
from apps.arts.models import ArtForm
from apps.cuisine.models import CuisineDish
from apps.core.models import TimelineEvent
from apps.quiz.models import QuizQuestion

@pytest.mark.django_db
def test_seed_data_command():
    call_command('seed_data')
    call_command('check_images')

    assert State.objects.count() >= 28, "Must have at least 28 states & UTs"
    assert HeritageSite.objects.count() >= 25, "Must have at least 25 heritage sites"
    assert Festival.objects.count() >= 20, "Must have at least 20 festivals"
    assert ArtForm.objects.count() >= 20, "Must have at least 20 art forms"
    assert CuisineDish.objects.count() >= 20, "Must have at least 20 dishes"
    assert QuizQuestion.objects.count() >= 30, "Must have at least 30 quiz questions"
    assert TimelineEvent.objects.count() >= 15, "Must have at least 15 timeline events"

    # Verify iconic UNESCO sites are present
    assert HeritageSite.objects.filter(name__icontains="Taj Mahal").exists()
    assert HeritageSite.objects.filter(name__icontains="Hampi").exists()
    assert HeritageSite.objects.filter(name__icontains="Khajuraho").exists()
    assert HeritageSite.objects.filter(name__icontains="Ajanta").exists()
    assert HeritageSite.objects.filter(name__icontains="Konark").exists()
