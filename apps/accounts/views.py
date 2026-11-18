from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView, View
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, JsonResponse
from .models import Bookmark, UserProfile
from .forms import RegistrationForm, UserProfileForm
from apps.heritage.models import HeritageSite
from apps.quiz.models import QuizScore
from apps.stories.models import Story

class CustomLoginView(BaseLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return super().form_valid(form)


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:home')
        form = RegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, f"Welcome to Virasat, {user.username}! Your cultural explorer profile has been created.")
            return redirect('accounts:profile')
        return render(request, 'accounts/register.html', {'form': form})


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })
        scores = QuizScore.objects.filter(user=request.user).order_by('-created_at')[:5]
        bookmarks_count = Bookmark.objects.filter(user=request.user).count()
        stories = Story.objects.filter(author=request.user)
        
        return render(request, 'accounts/profile.html', {
            'profile': profile,
            'form': form,
            'scores': scores,
            'bookmarks_count': bookmarks_count,
            'stories': stories,
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.save()
            messages.success(request, "Your profile details have been preserved successfully.")
            return redirect('accounts:profile')
        return render(request, 'accounts/profile.html', {'profile': profile, 'form': form})


class BookmarksView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        bookmarks = Bookmark.objects.filter(user=request.user).select_related('content_type')
        return render(request, 'accounts/bookmarks.html', {'bookmarks': bookmarks})


def toggle_bookmark(request):
    """HTMX endpoint to toggle bookmark state on any model object."""
    if not request.user.is_authenticated:
        return HttpResponse("""
            <a href="/accounts/login/" class="text-xs text-amber-500 font-bold hover:underline">
                Sign in to save
            </a>
        """)

    content_type_model = request.GET.get('content_type', '').lower()
    object_id = request.GET.get('object_id')

    try:
        ct = ContentType.objects.get(model=content_type_model)
        existing = Bookmark.objects.filter(user=request.user, content_type=ct, object_id=object_id).first()
        
        if existing:
            existing.delete()
            is_bookmarked = False
        else:
            Bookmark.objects.create(user=request.user, content_type=ct, object_id=object_id)
            is_bookmarked = True

        return render(request, 'accounts/partials/bookmark_button.html', {
            'is_bookmarked': is_bookmarked,
            'content_type': content_type_model,
            'object_id': object_id,
        })
    except Exception:
        return HttpResponse("Unable to toggle bookmark", status=400)
