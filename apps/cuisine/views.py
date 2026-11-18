from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.db.models import Q
from .models import CuisineDish
from apps.states.models import State

class CuisineListView(ListView):
    model = CuisineDish
    template_name = 'cuisine/list.html'
    context_object_name = 'dishes'
    paginate_by = 12

    def get_queryset(self):
        qs = CuisineDish.objects.select_related('state').order_by('state__name', 'name')
        
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(ingredients__icontains=q) | Q(story__icontains=q))

        diet = self.request.GET.get('diet', '').strip()
        if diet in ['veg', 'non-veg']:
            qs = qs.filter(veg_or_non_veg=diet)

        meal = self.request.GET.get('meal', '').strip()
        if meal:
            qs = qs.filter(meal_type__iexact=meal)

        state_slug = self.request.GET.get('state', '').strip()
        if state_slug:
            qs = qs.filter(state__slug=state_slug)

        spice = self.request.GET.get('spice', '').strip()
        if spice:
            qs = qs.filter(spice_level__icontains=spice)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['states'] = State.objects.filter(dishes__isnull=False).distinct().order_by('name')
        ctx['meal_types'] = [m[0] for m in CuisineDish.MEAL_CHOICES]
        ctx['spice_levels'] = [s[0] for s in CuisineDish.SPICE_CHOICES]
        ctx['selected_diet'] = self.request.GET.get('diet', '')
        ctx['selected_meal'] = self.request.GET.get('meal', '')
        ctx['selected_state'] = self.request.GET.get('state', '')
        ctx['selected_spice'] = self.request.GET.get('spice', '')
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('HX-Request'):
            return render(self.request, 'cuisine/partials/cuisine_grid.html', context)
        return super().render_to_response(context, **response_kwargs)


class CuisineDetailView(DetailView):
    model = CuisineDish
    template_name = 'cuisine/detail.html'
    context_object_name = 'dish'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        dish = self.object
        ctx['related_dishes'] = CuisineDish.objects.filter(
            Q(state=dish.state) | Q(veg_or_non_veg=dish.veg_or_non_veg)
        ).exclude(pk=dish.pk)[:3]
        return ctx
