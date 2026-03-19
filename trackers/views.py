from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Avg, Count
from .models import DailyLog, Habit, HabitLog, Expense, LearningLog


@login_required
def habit_tracker(request):
    today = timezone.now().date()
    habits = Habit.objects.filter(user=request.user, is_active=True)
    
    # Get which habits are completed today
    completed_today = set(
        HabitLog.objects.filter(
            habit__user=request.user, date=today, completed=True
        ).values_list('habit_id', flat=True)
    )

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_habit':
            name = request.POST.get('name', '').strip()
            emoji = request.POST.get('emoji', '✅').strip() or '✅'
            frequency = request.POST.get('frequency', 'daily')
            description = request.POST.get('description', '').strip()
            if name:
                Habit.objects.create(
                    user=request.user, name=name, emoji=emoji,
                    frequency=frequency, description=description
                )
                messages.success(request, f'Habit "{name}" created!')
            return redirect('habit_tracker')

        elif action == 'toggle':
            habit_id = request.POST.get('habit_id')
            try:
                habit = Habit.objects.get(id=habit_id, user=request.user)
                log, created = HabitLog.objects.get_or_create(habit=habit, date=today)
                if not created:
                    log.completed = not log.completed
                    log.save()
                else:
                    log.completed = True
                    log.save()
            except Habit.DoesNotExist:
                pass
            return redirect('habit_tracker')

        elif action == 'delete_habit':
            habit_id = request.POST.get('habit_id')
            Habit.objects.filter(id=habit_id, user=request.user).delete()
            messages.success(request, 'Habit removed.')
            return redirect('habit_tracker')

    context = {
        'habits': habits,
        'completed_today': completed_today,
        'today': today,
        'total_habits': habits.count(),
        'completed_count': len(completed_today),
    }
    return render(request, 'trackers/habits.html', context)


@login_required
def daily_log(request):
    today = timezone.now().date()
    existing = DailyLog.objects.filter(user=request.user, date=today).first()

    if request.method == 'POST':
        mood = int(request.POST.get('mood', 5))
        energy = int(request.POST.get('energy', 5))
        note = request.POST.get('note', '').strip()
        sleep_hours = request.POST.get('sleep_hours') or None

        if existing:
            existing.mood = mood
            existing.energy = energy
            existing.note = note
            existing.sleep_hours = sleep_hours
            existing.save()
            messages.success(request, 'Daily log updated!')
        else:
            DailyLog.objects.create(
                user=request.user, date=today, mood=mood,
                energy=energy, note=note, sleep_hours=sleep_hours
            )
            messages.success(request, "Today's log saved!")
        return redirect('daily_log')

    recent_logs = DailyLog.objects.filter(user=request.user).order_by('-date')[:14]
    context = {
        'existing': existing,
        'recent_logs': recent_logs,
        'today': today,
    }
    return render(request, 'trackers/daily_log.html', context)


@login_required
def expense_tracker(request):
    today = timezone.now().date()
    user_expenses = Expense.objects.filter(user=request.user).order_by('-date')

    if request.method == 'POST':
        amount = request.POST.get('amount', 0)
        category = request.POST.get('category', 'other')
        note = request.POST.get('note', '').strip()
        date_str = request.POST.get('date', '')
        try:
            from datetime import date
            log_date = date.fromisoformat(date_str) if date_str else today
            Expense.objects.create(
                user=request.user, amount=float(amount),
                category=category, note=note, date=log_date
            )
            messages.success(request, f'Expense of ₹{amount} logged!')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid data. Please check your inputs.')
        return redirect('expense_tracker')

    # Monthly total
    import datetime
    first_day = today.replace(day=1)
    monthly_total = user_expenses.filter(date__gte=first_day).aggregate(
        total=Sum('amount'))['total'] or 0

    # Category breakdown for chart
    from itertools import groupby
    cat_data = {}
    for exp in user_expenses.filter(date__gte=first_day):
        cat_data[exp.get_category_display()] = cat_data.get(exp.get_category_display(), 0) + float(exp.amount)

    import json
    context = {
        'expenses': user_expenses[:30],
        'monthly_total': monthly_total,
        'today': today.isoformat(),
        'category_labels': json.dumps(list(cat_data.keys())),
        'category_data': json.dumps(list(cat_data.values())),
        'category_choices': Expense._meta.get_field('category').choices,
    }
    return render(request, 'trackers/expenses.html', context)


@login_required
def learning_log(request):
    today = timezone.now().date()
    logs = LearningLog.objects.filter(user=request.user).order_by('-date')

    if request.method == 'POST':
        topic = request.POST.get('topic', '').strip()
        source = request.POST.get('source', '').strip()
        duration = request.POST.get('duration_minutes', 0)
        notes = request.POST.get('notes', '').strip()
        date_str = request.POST.get('date', '')
        try:
            from datetime import date
            log_date = date.fromisoformat(date_str) if date_str else today
            LearningLog.objects.create(
                user=request.user, topic=topic, source=source,
                duration_minutes=int(duration), notes=notes, date=log_date
            )
            messages.success(request, f'Logged {duration} mins on "{topic}"!')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid data submitted.')
        return redirect('learning_log')

    total_minutes = logs.aggregate(total=Sum('duration_minutes'))['total'] or 0
    context = {
        'logs': logs[:30],
        'today': today.isoformat(),
        'total_minutes': total_minutes,
        'total_hours': round(total_minutes / 60, 1),
    }
    return render(request, 'trackers/learning.html', context)
