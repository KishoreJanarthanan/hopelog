from django.urls import path
from . import views

urlpatterns = [
    path('habits/', views.habit_tracker, name='habit_tracker'),
    path('daily-log/', views.daily_log, name='daily_log'),
    path('expenses/', views.expense_tracker, name='expense_tracker'),
    path('learning/', views.learning_log, name='learning_log'),
]
