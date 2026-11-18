from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.db.models import Q
from .models import ArtForm
from apps.states.models import State

class ArtListView(ListView):
    model = ArtForm
    template_name = 'arts/list.html'
    context_object_name = 'arts'
    paginate_by = 12

    def get_queryset(self):
        qs = ArtForm.objects.select_related('origin_state').order_by('name')
        
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(famous_practitioners__icontains=q))

        category = self.request.GET.get('category', '').strip()
        if category:
            qs = qs.filter(category__iexact=category)

        state_slug = self.request.GET.get('state', '').strip()
        if state_slug:
            qs = qs.filter(origin_state__slug=state_slug)

        unesco = self.request.GET.get('unesco', '').strip()
        if unesco in ['1', 'true', 'True']:
            qs = qs.filter(unesco_intangible=True)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = [c[0] for c in ArtForm.CATEGORY_CHOICES]
        ctx['states'] = State.objects.filter(art_forms__isnull=False).distinct().order_by('name')
        ctx['selected_category'] = self.request.GET.get('category', '')
        ctx['selected_state'] = self.request.GET.get('state', '')
        ctx['selected_unesco'] = self.request.GET.get('unesco', '')
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('HX-Request'):
            return render(self.request, 'arts/partials/art_grid.html', context)
        return super().render_to_response(context, **response_kwargs)


class ArtDetailView(DetailView):
    model = ArtForm
    template_name = 'arts/detail.html'
    context_object_name = 'art'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        art = self.object
        ctx['related_arts'] = ArtForm.objects.filter(
            category=art.category
        ).exclude(pk=art.pk)[:3]
        return ctx
