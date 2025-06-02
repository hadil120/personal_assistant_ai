# agents/forms.py
from django import forms
from .models import Agent, Task

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['name']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']