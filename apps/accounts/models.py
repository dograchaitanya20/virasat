from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.URLField(max_length=500, blank=True, default='https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80')
    bio = models.TextField(blank=True, default='Cultural heritage enthusiast exploring the living arts of India.')
    location = models.CharField(max_length=150, blank=True, default='New Delhi, India')
    favorite_state = models.CharField(max_length=100, blank=True, default='Rajasthan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Bookmarks'
        constraints = [
            models.UniqueConstraint(fields=['user', 'content_type', 'object_id'], name='unique_user_bookmark')
        ]

    def __str__(self):
        return f"{self.user.username} bookmarked {self.content_object}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
