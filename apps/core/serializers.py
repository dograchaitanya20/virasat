from rest_framework import serializers
from apps.states.models import State
from apps.heritage.models import HeritageSite
from apps.festivals.models import Festival
from apps.arts.models import ArtForm
from apps.cuisine.models import CuisineDish
from apps.core.models import TimelineEvent

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'slug', 'capital', 'region', 'languages', 'summary', 'lat', 'lng', 'hero_image']

class HeritageSiteSerializer(serializers.ModelSerializer):
    state_name = serializers.ReadOnlyField(source='state.name')

    class Meta:
        model = HeritageSite
        fields = ['id', 'name', 'slug', 'state_name', 'category', 'unesco', 'unesco_year', 'era', 'built_by', 'built_year', 'architecture_style', 'description', 'lat', 'lng', 'hero_image']

class FestivalSerializer(serializers.ModelSerializer):
    states = serializers.StringRelatedField(many=True)

    class Meta:
        model = Festival
        fields = ['id', 'name', 'slug', 'month', 'approximate_dates', 'religion_or_type', 'significance', 'rituals', 'food', 'hero_image', 'states']

class ArtFormSerializer(serializers.ModelSerializer):
    origin_state_name = serializers.ReadOnlyField(source='origin_state.name')

    class Meta:
        model = ArtForm
        fields = ['id', 'name', 'slug', 'category', 'origin_state_name', 'history', 'description', 'famous_practitioners', 'unesco_intangible', 'hero_image']

class CuisineDishSerializer(serializers.ModelSerializer):
    state_name = serializers.ReadOnlyField(source='state.name')

    class Meta:
        model = CuisineDish
        fields = ['id', 'name', 'slug', 'state_name', 'veg_or_non_veg', 'meal_type', 'spice_level', 'cooking_time', 'ingredients', 'story', 'hero_image']

class TimelineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = ['id', 'year_era', 'year_numeric', 'title', 'slug', 'category', 'description', 'hero_image']
