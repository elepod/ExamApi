from django.contrib import admin

from api_habits.models import Category, Habit, HabitLog, User

# Register your models here.
admin.site.register(Category)
admin.site.register(Habit)
admin.site.register(HabitLog)
admin.site.register(User)
