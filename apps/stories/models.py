from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

class Story(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft (Private)'),
        ('pending', 'Pending Editorial Review'),
        ('published', 'Published to Living Archives'),
    ]

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    excerpt = models.TextField(help_text="Brief 1-2 sentence preview")
    body = models.TextField(help_text="Full community narrative, folklore or personal reflection")
    tags = models.CharField(max_length=200, help_text="Comma-separated topics e.g. temples, folklore, ritual")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    cover_image = models.CharField(max_length=500, blank=True, help_text="High-res photo URL or local static path")
    image_credit = models.CharField(max_length=255, blank=True, default="", help_text="Author or attribution")
    image_source_url = models.URLField(max_length=500, blank=True, default="", help_text="Source URL on Wikimedia Commons")
    image_license = models.CharField(max_length=100, blank=True, default="", help_text="Image license e.g. CC BY-SA 4.0")
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cultural Story'
        verbose_name_plural = 'Cultural Stories'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "story"
            slug = base_slug
            counter = 1
            while Story.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('stories:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.title} by {self.author.username}"
