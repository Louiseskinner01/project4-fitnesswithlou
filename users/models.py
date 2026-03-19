from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):

    EXPERIENCE_LEVEL = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    FITNESS_GOALS = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('general_fitness', 'General Fitness'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fitness_goal = models.CharField(max_length=50, choices=FITNESS_GOALS, blank=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL, blank=True)
    preferred_training_time = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username