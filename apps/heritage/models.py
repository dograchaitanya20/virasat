from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from apps.states.models import State

class HeritageSite(models.Model):
    CATEGORY_CHOICES = [
        ('Monument', 'Monument & Architecture'),
        ('Temple', 'Sacred Temple'),
        ('Fort', 'Royal Fort & Palace'),
        ('Cave', 'Ancient Cave & Rock-cut'),
        ('Natural', 'Natural Sanctuary'),
        ('Living Heritage', 'Living Heritage & Sacred City'),
    ]

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='heritage_sites')
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default='Monument')
    unesco = models.BooleanField(default=False, help_text="Is UNESCO World Heritage Site?")
    unesco_year = models.IntegerField(null=True, blank=True, help_text="Year inscribed by UNESCO")
    era = models.CharField(max_length=150, help_text="Historical period / dynasty")
    built_by = models.CharField(max_length=200, blank=True, help_text="Ruler, dynasty or patron")
    built_year = models.CharField(max_length=100, blank=True, help_text="Estimated century or year")
    architecture_style = models.CharField(max_length=150, blank=True, help_text="e.g. Dravidian, Nagara, Indo-Islamic")
    description = models.TextField(help_text="Detailed overview for travellers and students")
    history = models.TextField(help_text="In-depth historical narrative and inscriptions")
    visiting_info = models.TextField(help_text="Timings, entry fees, photography rules, best season")
    lat = models.FloatField(help_text="Latitude")
    lng = models.FloatField(help_text="Longitude")
    hero_image = models.CharField(max_length=500, help_text="Hero banner image URL or local path")
    image_credit = models.CharField(max_length=255, blank=True, default="", help_text="Author or attribution")
    image_source_url = models.URLField(max_length=500, blank=True, default="", help_text="Source URL on Wikimedia Commons")
    image_license = models.CharField(max_length=100, blank=True, default="", help_text="Image license e.g. CC BY-SA 4.0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Heritage Site'
        verbose_name_plural = 'Heritage Sites'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['unesco']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('heritage:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.name} ({self.state.name})"


class HeritageSiteImage(models.Model):
    site = models.ForeignKey(HeritageSite, on_delete=models.CASCADE, related_name='gallery_images')
    image_url = models.CharField(max_length=500)
    caption = models.CharField(max_length=255, blank=True)
    attribution = models.CharField(max_length=255, default="Wikimedia Commons / Royalty-Free")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Heritage Gallery Image'
        verbose_name_plural = 'Heritage Gallery Images'

    def __str__(self):
        return f"Image for {self.site.name} - {self.caption or self.id}"
