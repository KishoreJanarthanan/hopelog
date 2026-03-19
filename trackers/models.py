from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


MOOD_CHOICES = [(i, str(i)) for i in range(1, 11)]
ENERGY_CHOICES = [(i, str(i)) for i in range(1, 11)]

CATEGORY_CHOICES = [
    ('food', 'Food & Dining'),
    ('transport', 'Transport'),
    ('shopping', 'Shopping'),
    ('health', 'Health & Fitness'),
    ('entertainment', 'Entertainment'),
    ('education', 'Education'),
    ('bills', 'Bills & Utilities'),
    ('other', 'Other'),
]

FREQUENCY_CHOICES = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
]


class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, unique=False)
    mood = models.IntegerField(choices=MOOD_CHOICES, default=5)
    energy = models.IntegerField(choices=ENERGY_CHOICES, default=5)
    note = models.TextField(blank=True)
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} — {self.date}"


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    emoji = models.CharField(max_length=10, default='✅')
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} — {self.name}"


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=True)

    class Meta:
        unique_together = ['habit', 'date']

    def __str__(self):
        status = "✅" if self.completed else "❌"
        return f"{status} {self.habit.name} — {self.date}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} — ₹{self.amount} ({self.category})"


class LearningLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    topic = models.CharField(max_length=200)
    source = models.CharField(max_length=200, blank=True, help_text="Book, course, YouTube, etc.")
    duration_minutes = models.PositiveIntegerField(help_text="Minutes spent learning")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} — {self.topic} ({self.date})"
