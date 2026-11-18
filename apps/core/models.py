from django.db import models
from django.utils.text import slugify
from apps.heritage.models import HeritageSite

class TimelineEvent(models.Model):
    CATEGORY_CHOICES = [
        ('Ancient', 'Ancient Civilization (3000 BCE - 500 CE)'),
        ('Classical', 'Classical & Golden Dynasties (500 CE - 1200 CE)'),
        ('Medieval', 'Medieval & Imperial Era (1200 CE - 1750 CE)'),
        ('Colonial', 'Colonial & Resistance Period (1750 CE - 1947 CE)'),
        ('Modern', 'Sovereign Republic & Renaissance (1947 CE - Present)'),
    ]

    year_era = models.CharField(max_length=100, help_text="e.g. c. 2600 – 1900 BCE, 1509–1529 CE")
    year_numeric = models.IntegerField(help_text="Numeric year for accurate chronological sorting (-2600 for BCE)")
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='Ancient')
    description = models.TextField(help_text="Historical significance, cultural milestones and legacy")
    related_site = models.ForeignKey(HeritageSite, null=True, blank=True, on_delete=models.SET_NULL, related_name='timeline_events')
    hero_image = models.CharField(max_length=500, help_text="High-res archival image URL or local static path")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['year_numeric']
        verbose_name = 'Timeline Milestone'
        verbose_name_plural = 'Timeline Milestones'
        indexes = [
            models.Index(fields=['year_numeric']),
            models.Index(fields=['category']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.year_era} — {self.title}"
