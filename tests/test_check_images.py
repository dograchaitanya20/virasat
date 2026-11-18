import os
import shutil
import pytest
from pathlib import Path
from django.core.management import call_command, CommandError
from django.conf import settings

from apps.states.models import State
from apps.heritage.models import HeritageSite
from apps.festivals.models import Festival

def make_state(name="Test State"):
    return State.objects.create(
        name=name,
        capital="City",
        languages="Hindi, English",
        summary="A cultural state",
        lat=28.0,
        lng=77.0,
        region="North",
        famous_for="Heritage"
    )

def make_site(name, state, **kwargs):
    defaults = {
        'era': 'Ancient',
        'description': 'Description',
        'history': 'History narrative',
        'visiting_info': 'Timings 9am-5pm',
        'lat': 28.0,
        'lng': 77.0,
        'hero_image': '/static/images/placeholder.svg',
        'image_credit': 'Author',
        'image_source_url': 'https://commons.wikimedia.org/wiki/File:Test.jpg',
        'image_license': 'CC BY-SA 4.0'
    }
    defaults.update(kwargs)
    return HeritageSite.objects.create(name=name, state=state, **defaults)

def make_festival(name, **kwargs):
    defaults = {
        'approximate_dates': 'October',
        'significance': 'Significance',
        'rituals': 'Rituals',
        'food': 'Food',
        'story': 'Story legend',
        'hero_image': '/static/images/placeholder.svg',
        'image_credit': 'Author',
        'image_source_url': 'https://commons.wikimedia.org/wiki/File:Test.jpg',
        'image_license': 'CC BY-SA 4.0'
    }
    defaults.update(kwargs)
    return Festival.objects.create(name=name, **defaults)

@pytest.mark.django_db
def test_check_images_fails_on_missing_file(tmp_path):
    state = make_state("Missing State")
    make_site(
        "Missing Site",
        state=state,
        hero_image="/static/images/heritage/non-existent-file.jpg"
    )
    with pytest.raises(CommandError) as exc_info:
        call_command('check_images')
    assert "Image validation check failed" in str(exc_info.value)

@pytest.mark.django_db
def test_check_images_fails_on_empty_credit(tmp_path):
    static_dir = Path(settings.BASE_DIR) / 'static' / 'images' / 'heritage'
    static_dir.mkdir(parents=True, exist_ok=True)
    test_img = static_dir / '_test_dummy.jpg'
    test_img.write_bytes(b"dummy image data for testing")

    try:
        state = make_state("State Credit")
        make_site(
            "Uncredited Site",
            state=state,
            hero_image="/static/images/heritage/_test_dummy.jpg",
            image_credit="",  # Missing credit!
        )
        with pytest.raises(CommandError) as exc_info:
            call_command('check_images')
        assert "Image validation check failed" in str(exc_info.value)
    finally:
        if test_img.exists():
            test_img.unlink()

@pytest.mark.django_db
def test_check_images_fails_on_shared_file():
    static_dir = Path(settings.BASE_DIR) / 'static' / 'images' / 'heritage'
    static_dir.mkdir(parents=True, exist_ok=True)
    test_img = static_dir / '_test_shared.jpg'
    test_img.write_bytes(b"shared image content data")

    try:
        state = make_state("State Shared")
        make_site(
            "Site Alpha",
            state=state,
            hero_image="/static/images/heritage/_test_shared.jpg",
            image_credit="Author Alpha",
        )
        make_site(
            "Site Beta",
            state=state,
            hero_image="/static/images/heritage/_test_shared.jpg",
            image_credit="Author Beta",
        )
        with pytest.raises(CommandError) as exc_info:
            call_command('check_images')
        assert "Image validation check failed" in str(exc_info.value)
    finally:
        if test_img.exists():
            test_img.unlink()

@pytest.mark.django_db
def test_check_images_fails_on_identical_hash():
    static_dir = Path(settings.BASE_DIR) / 'static' / 'images' / 'heritage'
    static_dir.mkdir(parents=True, exist_ok=True)
    img1 = static_dir / '_test_hash1.jpg'
    img2 = static_dir / '_test_hash2.jpg'
    duplicate_content = b"identical image bytes for hash check"
    img1.write_bytes(duplicate_content)
    img2.write_bytes(duplicate_content)

    try:
        state = make_state("State Hash")
        make_site(
            "Site Gamma",
            state=state,
            hero_image="/static/images/heritage/_test_hash1.jpg",
            image_credit="Author Gamma",
        )
        make_festival(
            "Festival Gamma",
            hero_image="/static/images/heritage/_test_hash2.jpg",
            image_credit="Author Delta",
        )
        with pytest.raises(CommandError) as exc_info:
            call_command('check_images')
        assert "Image validation check failed" in str(exc_info.value)
    finally:
        if img1.exists():
            img1.unlink()
        if img2.exists():
            img2.unlink()

@pytest.mark.django_db
def test_check_images_passes_on_seeded_database():
    call_command('seed_data')
    # check_images must pass cleanly on the seeded database
    call_command('check_images')


