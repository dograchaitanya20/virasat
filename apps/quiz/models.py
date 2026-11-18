from django.db import models
from django.contrib.auth.models import User

class QuizQuestion(models.Model):
    OPTION_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    DIFFICULTY_CHOICES = [
        ('Easy', 'Explorer (Easy)'),
        ('Medium', 'Scholar (Medium)'),
        ('Hard', 'Archivist (Challenging)'),
    ]

    CATEGORY_CHOICES = [
        ('Monuments', 'Monuments & Architecture'),
        ('Festivals', 'Festivals & Sacred Calendar'),
        ('Arts & Music', 'Classical Arts & Dances'),
        ('History', 'Dynasties & History'),
        ('Cuisine', 'Regional Culinary Traditions'),
    ]

    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES)
    explanation = models.TextField(help_text="Fascinating context and historical fact explaining the answer")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Medium')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='Monuments')

    class Meta:
        verbose_name = 'Quiz Question'
        verbose_name_plural = 'Quiz Questions'
        indexes = [
            models.Index(fields=['difficulty']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"[{self.category}] {self.question[:60]}..."


class QuizScore(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='quiz_scores')
    player_name = models.CharField(max_length=100, default='Heritage Explorer')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=10)
    percentage = models.FloatField(default=0.0)
    time_taken_seconds = models.IntegerField(default=60)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', 'time_taken_seconds', '-created_at']
        verbose_name = 'Quiz Leaderboard Score'
        verbose_name_plural = 'Quiz Leaderboard Scores'

    def save(self, *args, **kwargs):
        if self.total_questions > 0:
            self.percentage = round((self.score / self.total_questions) * 100, 1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player_name}: {self.score}/{self.total_questions} ({self.percentage}%)"
