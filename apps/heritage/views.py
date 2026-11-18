from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import HeritageSite
from apps.states.models import State

class HeritageListView(ListView):
    model = HeritageSite
    template_name = 'heritage/list.html'
    context_object_name = 'sites'
    paginate_by = 9

    def get_queryset(self):
        qs = HeritageSite.objects.select_related('state').order_by('name')
        
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(built_by__icontains=q))

        state_slug = self.request.GET.get('state', '').strip()
        if state_slug:
            qs = qs.filter(state__slug=state_slug)

        category = self.request.GET.get('category', '').strip()
        if category:
            qs = qs.filter(category__iexact=category)

        unesco = self.request.GET.get('unesco', '').strip()
        if unesco in ['1', 'true', 'True']:
            qs = qs.filter(unesco=True)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_sites_count'] = HeritageSite.objects.count()
        ctx['states'] = State.objects.filter(heritage_sites__isnull=False).distinct().order_by('name')
        ctx['categories'] = [c[0] for c in HeritageSite.CATEGORY_CHOICES]
        ctx['selected_category'] = self.request.GET.get('category', '')
        ctx['selected_state'] = self.request.GET.get('state', '')
        ctx['selected_unesco'] = self.request.GET.get('unesco', '')
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('HX-Request'):
            return render(self.request, 'heritage/partials/site_grid.html', context)
        return super().render_to_response(context, **response_kwargs)


class HeritageDetailView(DetailView):
    model = HeritageSite
    template_name = 'heritage/detail.html'
    context_object_name = 'site'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        site = self.object
        ctx['gallery_images'] = site.gallery_images.all()
        ctx['related_sites'] = HeritageSite.objects.filter(
            Q(state=site.state) | Q(category=site.category)
        ).exclude(pk=site.pk).select_related('state')[:3]
        
        # Check if bookmarked
        is_bookmarked = False
        if self.request.user.is_authenticated:
            from django.contrib.contenttypes.models import ContentType
            from apps.accounts.models import Bookmark
            ct = ContentType.objects.get_for_model(HeritageSite)
            is_bookmarked = Bookmark.objects.filter(user=self.request.user, content_type=ct, object_id=site.id).exists()
        ctx['is_bookmarked'] = is_bookmarked
        return ctx
