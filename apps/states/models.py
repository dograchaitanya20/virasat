from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class State(models.Model):
    REGION_CHOICES = [
        ('North', 'North India'),
        ('South', 'South India'),
        ('East', 'East India'),
        ('West', 'West India'),
        ('Central', 'Central India'),
        ('Northeast', 'Northeast India'),
        ('UT', 'Union Territory'),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    capital = models.CharField(max_length=100)
    languages = models.CharField(max_length=200, help_text="Official and commonly spoken languages")
    summary = models.TextField(help_text="Comprehensive cultural summary")
    hero_image = models.CharField(max_length=500, help_text="High-res Wikimedia/SVG image URL or local path")
    image_credit = models.CharField(max_length=255, blank=True, default="", help_text="Author or attribution")
    image_source_url = models.URLField(max_length=500, blank=True, default="", help_text="Source URL")
    image_license = models.CharField(max_length=100, blank=True, default="", help_text="Image license")
    lat = models.FloatField(help_text="Latitude for map positioning")
    lng = models.FloatField(help_text="Longitude for map positioning")
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default='North')
    emblem_description = models.CharField(max_length=255, blank=True, help_text="State motif/symbol")
    best_time_to_visit = models.CharField(max_length=150, default="October to March")
    famous_for = models.CharField(max_length=255, help_text="Short key highlights")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'State & Region'
        verbose_name_plural = 'States & Regions'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['region']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('states:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
