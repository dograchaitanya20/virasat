from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from apps.states.models import State

class Festival(models.Model):
    MONTH_CHOICES = [
        (1, 'January (Magha)'),
        (2, 'February (Phalguna)'),
        (3, 'March (Chaitra)'),
        (4, 'April (Vaishakha)'),
        (5, 'May (Jyeshtha)'),
        (6, 'June (Ashadha)'),
        (7, 'July (Shravana)'),
        (8, 'August (Bhadrapada)'),
        (9, 'September (Ashwin)'),
        (10, 'October (Kartik)'),
        (11, 'November (Margashirsha)'),
        (12, 'December (Pausha)'),
    ]

    RELIGION_TYPE_CHOICES = [
        ('Pan-Indian', 'Pan-Indian Celebration'),
        ('Hinduism', 'Hindu Festival'),
        ('Islam', 'Islamic Festival'),
        ('Sikhism', 'Sikh Festival'),
        ('Buddhism', 'Buddhist Festival'),
        ('Jainism', 'Jain Festival'),
        ('Christianity', 'Christian Festival'),
        ('Tribal / Harvest', 'Tribal & Harvest Festival'),
    ]

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    states = models.ManyToManyField(State, related_name='festivals', blank=True)
    month = models.IntegerField(choices=MONTH_CHOICES, default=10)
    approximate_dates = models.CharField(max_length=150, help_text="Calendar duration or lunar tithi")
    religion_or_type = models.CharField(max_length=40, choices=RELIGION_TYPE_CHOICES, default='Pan-Indian')
    significance = models.TextField(help_text="Spiritual, agricultural or historical significance")
    rituals = models.TextField(help_text="Sacred rites, dances, processions and offerings")
    food = models.TextField(help_text="Traditional festive foods and sweets prepared")
    story = models.TextField(help_text="Legend, mythological tale or folklore associated")
    hero_image = models.CharField(max_length=500, help_text="High-res banner image URL or local path")
    image_credit = models.CharField(max_length=255, blank=True, default="", help_text="Author or attribution")
    image_source_url = models.URLField(max_length=500, blank=True, default="", help_text="Source URL on Wikimedia Commons")
    image_license = models.CharField(max_length=100, blank=True, default="", help_text="Image license e.g. CC BY-SA 4.0")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['month', 'name']
        verbose_name = 'Festival'
        verbose_name_plural = 'Festivals'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['month']),
            models.Index(fields=['is_featured']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('festivals:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
