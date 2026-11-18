from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from apps.states.models import State

class ArtForm(models.Model):
    CATEGORY_CHOICES = [
        ('Dance', 'Classical & Folk Dance'),
        ('Music', 'Vocal & Instrumental Music'),
        ('Painting', 'Folk & Miniature Painting'),
        ('Craft', 'Handicraft & Sculpture'),
        ('Textile', 'Weaving & Textile Heritage'),
        ('Theatre', 'Traditional Theatre & Puppetry'),
    ]

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='Dance')
    origin_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name='art_forms')
    history = models.TextField(help_text="Historical origin, texts (e.g. Natya Shastra) and evolution")
    description = models.TextField(help_text="Technique, instruments, mudras, motifs, or materials")
    famous_practitioners = models.TextField(help_text="Legends, gharanas, living master artisans")
    hero_image = models.CharField(max_length=500, help_text="High-res banner image URL or local path")
    image_credit = models.CharField(max_length=255, blank=True, default="", help_text="Author or attribution")
    image_source_url = models.URLField(max_length=500, blank=True, default="", help_text="Source URL on Wikimedia Commons")
    image_license = models.CharField(max_length=100, blank=True, default="", help_text="Image license e.g. CC BY-SA 4.0")
    unesco_intangible = models.BooleanField(default=False, help_text="Inscribed on UNESCO Intangible Cultural Heritage List")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Art Form & Craft'
        verbose_name_plural = 'Art Forms & Crafts'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['unesco_intangible']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('arts:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
