from django import forms

from .models import Reminder

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'start_datetime', 'period', 'active', 'sms', 'email']