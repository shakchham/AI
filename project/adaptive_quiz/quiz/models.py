from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    DIFFICULTY_CHOICES = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )

    text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return f"{self.text[:50]}... ({self.difficulty})"

class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    current_difficulty = models.CharField(max_length=10, choices=Question.DIFFICULTY_CHOICES, default='Easy')

    def __str__(self):
        return f"{self.user.username} - {self.score} pts"
