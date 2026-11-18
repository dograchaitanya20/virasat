from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime
from .models import Festival
from apps.states.models import State

class FestivalListView(ListView):
    model = Festival
    template_name = 'festivals/list.html'
    context_object_name = 'festivals'
    paginate_by = 12

    def get_queryset(self):
        qs = Festival.objects.prefetch_related('states').order_by('month', 'name')
        
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(significance__icontains=q) | Q(food__icontains=q))

        month = self.request.GET.get('month', '').strip()
        if month and month.isdigit():
            qs = qs.filter(month=int(month))

        religion = self.request.GET.get('religion', '').strip()
        if religion:
            qs = qs.filter(religion_or_type__iexact=religion)

        state_slug = self.request.GET.get('state', '').strip()
        if state_slug:
            qs = qs.filter(states__slug=state_slug)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        current_month = datetime.now().month
        ctx['current_month'] = current_month
        ctx['months'] = [
            (1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'),
            (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'),
            (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')
        ]
        ctx['religions'] = [r[0] for r in Festival.RELIGION_TYPE_CHOICES]
        ctx['states'] = State.objects.filter(festivals__isnull=False).distinct().order_by('name')
        ctx['selected_month'] = self.request.GET.get('month', '')
        ctx['selected_religion'] = self.request.GET.get('religion', '')
        ctx['selected_state'] = self.request.GET.get('state', '')
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('HX-Request'):
            return render(self.request, 'festivals/partials/festival_grid.html', context)
        return super().render_to_response(context, **response_kwargs)


class FestivalDetailView(DetailView):
    model = Festival
    template_name = 'festivals/detail.html'
    context_object_name = 'festival'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        fest = self.object
        ctx['associated_states'] = fest.states.all()
        ctx['related_festivals'] = Festival.objects.filter(
            Q(month=fest.month) | Q(religion_or_type=fest.religion_or_type)
        ).exclude(pk=fest.pk)[:3]
        return ctx
