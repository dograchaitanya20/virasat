from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics

from apps.states.models import State
from apps.heritage.models import HeritageSite
from apps.festivals.models import Festival
from apps.arts.models import ArtForm
from apps.cuisine.models import CuisineDish
from apps.core.models import TimelineEvent
from .serializers import (
    StateSerializer,
    HeritageSiteSerializer,
    FestivalSerializer,
    ArtFormSerializer,
    CuisineDishSerializer,
    TimelineEventSerializer
)

@api_view(['GET'])
@permission_classes([AllowAny])
def stats_api(request):
    return Response({
        'status': 'online',
        'project': 'Virasat (विरासत)',
        'description': 'Interactive Digital Showcase of India\'s Cultural Heritage',
        'records': {
            'states': State.objects.count(),
            'heritage_sites': HeritageSite.objects.count(),
            'festivals': Festival.objects.count(),
            'art_forms': ArtForm.objects.count(),
            'dishes': CuisineDish.objects.count(),
            'timeline_milestones': TimelineEvent.objects.count(),
        }
    })

class StateListAPI(generics.ListAPIView):
    queryset = State.objects.all().order_by('name')
    serializer_class = StateSerializer
    permission_classes = [AllowAny]

class HeritageListAPI(generics.ListAPIView):
    queryset = HeritageSite.objects.select_related('state').order_by('name')
    serializer_class = HeritageSiteSerializer
    permission_classes = [AllowAny]

class FestivalListAPI(generics.ListAPIView):
    queryset = Festival.objects.prefetch_related('states').order_by('month', 'name')
    serializer_class = FestivalSerializer
    permission_classes = [AllowAny]

class ArtListAPI(generics.ListAPIView):
    queryset = ArtForm.objects.select_related('origin_state').order_by('name')
    serializer_class = ArtFormSerializer
    permission_classes = [AllowAny]

class CuisineListAPI(generics.ListAPIView):
    queryset = CuisineDish.objects.select_related('state').order_by('name')
    serializer_class = CuisineDishSerializer
    permission_classes = [AllowAny]

class TimelineListAPI(generics.ListAPIView):
    queryset = TimelineEvent.objects.all().order_by('year_numeric')
    serializer_class = TimelineEventSerializer
    permission_classes = [AllowAny]
