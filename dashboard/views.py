from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from trackers.models import DailyLog, Habit, HabitLog, Expense, LearningLog
from django.utils import timezone
from django.db.models import Sum, Avg, Count
import json


@login_required
def home(request):
    user = request.user
    today = timezone.now().date()

    # Today's daily log
    todays_log = DailyLog.objects.filter(user=user, date=today).first()

    # Habit stats today
    habits = Habit.objects.filter(user=user, is_active=True)
    habits_completed_today = HabitLog.objects.filter(
        habit__user=user, date=today, completed=True
    ).count()

    # Monthly expense total
    first_day = today.replace(day=1)
    monthly_expense = Expense.objects.filter(user=user, date__gte=first_day).aggregate(
        total=Sum('amount'))['total'] or 0

    # Total learning hours
    total_learn_minutes = LearningLog.objects.filter(user=user).aggregate(
        total=Sum('duration_minutes'))['total'] or 0

    # Mood trend (last 7 days)
    mood_labels = []
    mood_data = []
    for i in range(6, -1, -1):
        day = today - timezone.timedelta(days=i)
        log = DailyLog.objects.filter(user=user, date=day).first()
        mood_labels.append(day.strftime('%a'))
        mood_data.append(log.mood if log else None)

    # Recent activity (last 5 daily logs)
    recent_logs = DailyLog.objects.filter(user=user).order_by('-date')[:5]

    # Recent learning logs
    recent_learning = LearningLog.objects.filter(user=user).order_by('-date')[:5]

    context = {
        'todays_log': todays_log,
        'habits_total': habits.count(),
        'habits_completed_today': habits_completed_today,
        'monthly_expense': monthly_expense,
        'total_learn_hours': round(total_learn_minutes / 60, 1),
        'recent_logs': recent_logs,
        'recent_learning': recent_learning,
        'mood_labels': json.dumps(mood_labels),
        'mood_data': json.dumps(mood_data),
    }
    return render(request, 'dashboard/home.html', context)
