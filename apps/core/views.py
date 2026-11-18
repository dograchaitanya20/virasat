from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count
from django.views.decorators.http import require_POST
from datetime import datetime

from apps.states.models import State
from apps.heritage.models import HeritageSite
from apps.festivals.models import Festival
from apps.arts.models import ArtForm
from apps.cuisine.models import CuisineDish
from apps.core.models import TimelineEvent
from apps.stories.models import Story
from apps.quiz.models import QuizQuestion

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        current_month = datetime.now().month
        
        ctx['stats'] = {
            'states': State.objects.count(),
            'sites': HeritageSite.objects.count(),
            'festivals': Festival.objects.count(),
            'arts': ArtForm.objects.count(),
            'dishes': CuisineDish.objects.count(),
            'events': TimelineEvent.objects.count(),
        }
        ctx['featured_sites'] = HeritageSite.objects.filter(unesco=True).select_related('state')[:8]
        
        # Festival of the month: check current month first (featured or regular)
        festival = Festival.objects.filter(month=current_month, is_featured=True).first()
        if not festival:
            festival = Festival.objects.filter(month=current_month).first()

        is_current_month = bool(festival)
        if not festival:
            # Fall back to the next upcoming festival in the calendar
            festival = (
                Festival.objects.filter(month__gt=current_month, is_featured=True).order_by('month').first()
                or Festival.objects.filter(month__gt=current_month).order_by('month').first()
                or Festival.objects.filter(month__lt=current_month, is_featured=True).order_by('month').first()
                or Festival.objects.filter(month__lt=current_month).order_by('month').first()
                or Festival.objects.first()
            )

        ctx['festival_of_month'] = festival
        ctx['is_current_month_festival'] = is_current_month
        
        ctx['featured_arts'] = ArtForm.objects.select_related('origin_state')[:6]
        ctx['featured_stories'] = Story.objects.filter(status='published').select_related('author')[:3]
        ctx['timeline_sample'] = TimelineEvent.objects.all()[:4]
        return ctx

class MapView(TemplateView):
    template_name = 'core/map.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['states'] = State.objects.all().order_by('name')
        return ctx

class TimelineView(TemplateView):
    template_name = 'core/timeline.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['events'] = TimelineEvent.objects.select_related('related_site').order_by('year_numeric')
        return ctx

class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['heritage_credits'] = HeritageSite.objects.exclude(image_credit='').order_by('name')
        ctx['festival_credits'] = Festival.objects.exclude(image_credit='').order_by('name')
        ctx['art_credits'] = ArtForm.objects.exclude(image_credit='').order_by('name')
        ctx['cuisine_credits'] = CuisineDish.objects.exclude(image_credit='').order_by('name')
        ctx['story_credits'] = Story.objects.exclude(image_credit='').order_by('title')
        ctx['state_credits'] = State.objects.exclude(image_credit='').order_by('name')
        return ctx

class ContactView(TemplateView):
    template_name = 'core/contact.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        return render(request, 'core/contact.html', {
            'success_message': f'Thank you {name or "esteemed explorer"}, your message has been received. Our cultural archivist will respond within 24 hours.'
        })

class PrivacyView(TemplateView):
    template_name = 'core/privacy.html'

def quick_search(request):
    """HTMX quick search endpoint returning grouped search results."""
    query = request.GET.get('q', '').strip()
    if not query or len(query) < 2:
        return HttpResponse("""
            <div class="py-8 text-center text-slate-400 space-y-2">
                <p class="text-sm">Type at least 2 characters to search across monuments, festivals, crafts, dishes, and states...</p>
            </div>
        """)
    
    sites = HeritageSite.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))[:4]
    festivals = Festival.objects.filter(Q(name__icontains=query) | Q(significance__icontains=query))[:4]
    arts = ArtForm.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))[:4]
    dishes = CuisineDish.objects.filter(Q(name__icontains=query) | Q(ingredients__icontains=query))[:4]
    states = State.objects.filter(Q(name__icontains=query) | Q(famous_for__icontains=query))[:4]

    total_matches = sites.count() + festivals.count() + arts.count() + dishes.count() + states.count()

    if total_matches == 0:
        return HttpResponse(f"""
            <div class="py-8 text-center text-slate-400 space-y-2">
                <p class="text-sm">No cultural relics found matching "<strong>{query}</strong>".</p>
                <p class="text-xs text-slate-500">Try searching for Taj Mahal, Kathak, Diwali, Biryani, or Rajasthan.</p>
            </div>
        """)

    return render(request, 'core/partials/search_results.html', {
        'query': query,
        'sites': sites,
        'festivals': festivals,
        'arts': arts,
        'dishes': dishes,
        'states': states,
        'total_matches': total_matches,
    })

@require_POST
def newsletter_signup(request):
    email = request.POST.get('email', '').strip()
    return HttpResponse(f"""
        <div class="p-3 rounded-xl bg-emerald-900/40 border border-emerald-500/50 text-emerald-200 text-xs flex items-center gap-2">
            <svg class="w-4 h-4 text-emerald-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            <span>Welcome to Virasat Chronicles! We've sent an invitation to <strong>{email}</strong>.</span>
        </div>
    """)

def custom_404(request, exception=None):
    return render(request, 'core/404.html', status=404)

def custom_500(request):
    return render(request, 'core/500.html', status=500)
