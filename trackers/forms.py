from django import forms
from .models import DSAPractice, AptitudePractice, ForgeAttendance

class DSAPracticeForm(forms.ModelForm):
    class Meta:
        model = DSAPractice
        fields = ['date', 'platform', 'topic', 'problems_solved', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border'}),
            'platform': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border'}),
            'topic': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border', 'placeholder': 'e.g. Arrays, Dynamic Programming'}),
            'problems_solved': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border', 'min': '1'}),
            'notes': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border', 'rows': 3, 'placeholder': 'Optional notes...'}),
        }
