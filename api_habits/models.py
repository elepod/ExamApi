from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class User(AbstractUser):
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Habit(models.Model):
    habit_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='habits')
    period = models.TextField()
    description = models.TextField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.habit_name

class HabitLog(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='logs')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    execute_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return f"User {self.user.username} executed habit {self.habit} at {self.execute_date}"
