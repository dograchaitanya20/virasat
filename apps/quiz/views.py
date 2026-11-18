from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
import json
import random
from .models import QuizQuestion, QuizScore

class QuizPlayView(TemplateView):
    template_name = 'quiz/quiz_play.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Select 10 random questions
        all_ids = list(QuizQuestion.objects.values_list('id', flat=True))
        selected_ids = random.sample(all_ids, min(10, len(all_ids))) if all_ids else []
        questions = QuizQuestion.objects.filter(id__in=selected_ids)
        
        # Serialize questions to JSON for seamless Alpine.js state handling
        questions_payload = []
        for q in questions:
            questions_payload.append({
                'id': q.id,
                'question': q.question,
                'option_a': q.option_a,
                'option_b': q.option_b,
                'option_c': q.option_c,
                'option_d': q.option_d,
                'correct_option': q.correct_option,
                'explanation': q.explanation,
                'category': q.category,
                'difficulty': q.difficulty,
            })

        ctx['questions_json'] = json.dumps(questions_payload)
        ctx['total_questions'] = len(questions_payload)
        return ctx


@require_POST
def submit_score_api(request):
    """Saves player quiz performance to leaderboard."""
    try:
        data = json.loads(request.body)
        player_name = data.get('player_name', '').strip() or 'Anonymous Explorer'
        score = int(data.get('score', 0))
        total = int(data.get('total_questions', 10))
        time_taken = int(data.get('time_taken', 60))

        score_obj = QuizScore.objects.create(
            user=request.user if request.user.is_authenticated else None,
            player_name=player_name,
            score=score,
            total_questions=total,
            time_taken_seconds=time_taken
        )

        rank = QuizScore.objects.filter(score__gt=score).count() + 1

        return JsonResponse({
            'status': 'success',
            'id': score_obj.id,
            'rank': rank,
            'percentage': score_obj.percentage,
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class LeaderboardView(ListView):
    model = QuizScore
    template_name = 'quiz/leaderboard.html'
    context_object_name = 'scores'
    paginate_by = 25

    def get_queryset(self):
        return QuizScore.objects.all().order_by('-score', 'time_taken_seconds', '-created_at')
