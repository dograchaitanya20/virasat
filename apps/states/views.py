from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import State

class StateListView(ListView):
    model = State
    template_name = 'states/list.html'
    context_object_name = 'states'

    def get_queryset(self):
        qs = State.objects.all().order_by('name')
        region = self.request.GET.get('region', '').strip()
        if region:
            qs = qs.filter(region__iexact=region)
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(capital__icontains=q) | Q(famous_for__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['regions'] = [r[0] for r in State.REGION_CHOICES if State.objects.filter(region=r[0]).exists()]
        ctx['selected_region'] = self.request.GET.get('region', '')
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx


class StateDetailView(DetailView):
    model = State
    template_name = 'states/detail.html'
    context_object_name = 'state'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        state = self.object
        ctx['sites'] = state.heritage_sites.all()
        ctx['festivals'] = state.festivals.all()
        ctx['arts'] = state.art_forms.all()
        ctx['dishes'] = state.dishes.all()
        return ctx


def state_panel_partial(request, slug):
    """HTMX partial view rendering the side-panel drawer on the map page."""
    state = get_object_or_404(State, slug=slug)
    sites = state.heritage_sites.all()[:4]
    festivals = state.festivals.all()[:4]
    arts = state.art_forms.all()[:4]
    dishes = state.dishes.all()[:4]

    return render(request, 'states/partials/state_side_panel.html', {
        'state': state,
        'sites': sites,
        'festivals': festivals,
        'arts': arts,
        'dishes': dishes,
    })
