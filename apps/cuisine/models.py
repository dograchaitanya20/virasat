from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from apps.states.models import State

class CuisineDish(models.Model):
    DIET_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non-veg', 'Non-Vegetarian'),
    ]

    MEAL_CHOICES = [
        ('Main Course', 'Main Course'),
        ('Breakfast / Snack', 'Breakfast / Snack'),
        ('Dessert / Sweet', 'Dessert / Sweet'),
        ('Beverage / Brew', 'Beverage / Brew'),
    ]

    SPICE_CHOICES = [
        ('Mild', 'Mild & Aromatic'),
        ('Medium', 'Medium Spiced'),
        ('Fiery', 'Fiery & Robust'),
    ]

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='dishes')
    veg_or_non_veg = models.CharField(max_length=10, choices=DIET_CHOICES, default='veg')
    meal_type = models.CharField(max_length=30, choices=MEAL_CHOICES, default='Main Course')
    spice_level = models.CharField(max_length=20, choices=SPICE_CHOICES, default='Medium')
    cooking_time = models.CharField(max_length=50, default="45 mins")
    ingredients = models.TextField(help_text="Key spices, grains, herbs and signature components")
    story = models.TextField(help_text="Origin folklore, royal court or temple kitchen history")
    hero_image = models.CharField(max_length=500, help_text="High-res dish photography URL or local path")
    image_credit = models.CharField(max_length=255, blank=True, default="", help_text="Author or attribution")
    image_source_url = models.URLField(max_length=500, blank=True, default="", help_text="Source URL on Wikimedia Commons")
    image_license = models.CharField(max_length=100, blank=True, default="", help_text="Image license e.g. CC BY-SA 4.0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['state__name', 'name']
        verbose_name = 'Cuisine & Dish'
        verbose_name_plural = 'Cuisines & Dishes'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['veg_or_non_veg']),
            models.Index(fields=['meal_type']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cuisine:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.name} ({self.state.name})"
