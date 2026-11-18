from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import F
from .models import Story

class StoryListView(ListView):
    model = Story
    template_name = 'stories/list.html'
    context_object_name = 'stories'
    paginate_by = 9

    def get_queryset(self):
        return Story.objects.filter(status='published').select_related('author').order_by('-created_at')


class StoryDetailView(DetailView):
    model = Story
    template_name = 'stories/detail.html'
    context_object_name = 'story'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self):
        obj = super().get_object()
        # Increment views counter atomically
        Story.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['recent_stories'] = Story.objects.filter(status='published').exclude(pk=self.object.pk)[:3]
        return ctx


class StorySubmitView(LoginRequiredMixin, CreateView):
    model = Story
    template_name = 'stories/submit.html'
    fields = ['title', 'excerpt', 'body', 'tags', 'cover_image']

    def form_valid(self, form):
        story = form.save(commit=False)
        story.author = self.request.user
        # Automatically mark published so the user immediately sees it
        story.status = 'published'
        story.save()
        messages.success(self.request, "Your cultural story has been published to the Living Chronicles!")
        return redirect('stories:detail', slug=story.slug)
