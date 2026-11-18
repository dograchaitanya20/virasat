from django.contrib import admin
from .models import QuizQuestion, QuizScore

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_short', 'category', 'difficulty', 'correct_option')
    list_filter = ('category', 'difficulty', 'correct_option')
    search_fields = ('question', 'explanation')

    def question_short(self, obj):
        return obj.question[:70] + "..." if len(obj.question) > 70 else obj.question
    question_short.short_description = "Question"

@admin.register(QuizScore)
class QuizScoreAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'score', 'total_questions', 'percentage', 'time_taken_seconds', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('player_name',)
    ordering = ('-score', 'time_taken_seconds')
