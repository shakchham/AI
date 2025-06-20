from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Question, UserProgress
from .forms import SignupForm
import json

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProgress.objects.create(user=user)
            login(request, user)
            return redirect('quiz')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('quiz')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def quiz_view(request):
    progress, _ = UserProgress.objects.get_or_create(user=request.user)

    # Reset if quiz finished
    if request.session.get('question_count', 0) >= 10:
        final_score = progress.score
        request.session.flush()
        progress.score = 0
        progress.current_difficulty = 'Easy'
        progress.save()
        return render(request, 'quiz_end.html', {'score': final_score})

    # Initialize quiz session
    if 'question_count' not in request.session:
        request.session['question_count'] = 1
        request.session['asked_questions'] = []
    else:
        request.session['question_count'] += 1

    if request.session['question_count'] > 10:
        return render(request, 'quiz_end.html', {'score': progress.score})

    asked_ids = request.session.get('asked_questions', [])
    difficulty = progress.current_difficulty

    # Get a new question, not previously asked
    question = Question.objects.filter(difficulty=difficulty).exclude(id__in=asked_ids).order_by('?').first()

    if not question:
        return render(request, 'quiz_end.html', {'score': progress.score, 'error': 'No more questions available.'})

    # Track the question
    asked_ids.append(question.id)
    request.session['asked_questions'] = asked_ids
    request.session['question_id'] = question.id

    return render(request, 'quiz.html', {
        'question_number': request.session['question_count'],
        'question_text': question.text,
        'difficulty': question.difficulty,
        'options': [question.option1, question.option2, question.option3, question.option4],
        'score': progress.score,
        'progress': request.session['question_count']
    })

@login_required
def submit_answer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected = data.get('answer')
            question_id = request.session.get('question_id')
            question = Question.objects.get(id=question_id)
            progress = UserProgress.objects.get(user=request.user)

            if selected == question.correct_answer:
                progress.score += 1
                if progress.current_difficulty == 'Easy':
                    progress.current_difficulty = 'Medium'
                elif progress.current_difficulty == 'Medium':
                    progress.current_difficulty = 'Hard'
            else:
                if progress.current_difficulty == 'Hard':
                    progress.current_difficulty = 'Medium'
                elif progress.current_difficulty == 'Medium':
                    progress.current_difficulty = 'Easy'

            progress.save()
            return JsonResponse({'success': True, 'correct': selected == question.correct_answer})
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'success': False})

def logout_view(request):
    logout(request)
    return redirect('login')
