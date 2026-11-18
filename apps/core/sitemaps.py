from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.heritage.models import HeritageSite
from apps.festivals.models import Festival
from apps.arts.models import ArtForm
from apps.cuisine.models import CuisineDish
from apps.states.models import State
from apps.stories.models import Story

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return [
            'core:home',
            'core:map',
            'core:timeline',
            'core:about',
            'core:contact',
            'heritage:list',
            'festivals:list',
            'arts:list',
            'cuisine:list',
            'states:list',
            'stories:list',
            'quiz:play',
            'quiz:leaderboard',
        ]

    def location(self, item):
        return reverse(item)


class HeritageSiteSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return HeritageSite.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class FestivalSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Festival.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class ArtFormSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return ArtForm.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class CuisineSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return CuisineDish.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class StateSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return State.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class StorySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return Story.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at
