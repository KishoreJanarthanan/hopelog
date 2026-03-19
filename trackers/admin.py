from django.contrib import admin
from .models import DailyLog, Habit, HabitLog, Expense, LearningLog

@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'mood', 'energy', 'sleep_hours']
    list_filter = ['user']

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'frequency', 'is_active']

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ['habit', 'date', 'completed']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'amount', 'category', 'note']

@admin.register(LearningLog)
class LearningLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'topic', 'source', 'duration_minutes']
