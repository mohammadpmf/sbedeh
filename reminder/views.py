from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime
import jdatetime

from . import backend # برای این که کارها انجام بشن ایمپورت کردم. استفاده ای ازش نمیکنیم اینجا.
from .models import Reminder
from .forms import ReminderForm, ReminderFormToSHow



class HomePage(generic.TemplateView):
    template_name = 'enter_number.html'


class AllReminders(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        reminders = Reminder.objects.filter(user=user).order_by('-id')
        for reminder in reminders:
            reminder.form=ReminderFormToSHow(initial={
                'active' :reminder.active,
                'sms' :reminder.sms,
                'email' :reminder.email,
                'telegram' :reminder.telegram,
                'whatsapp' :reminder.whatsapp,
                'notification' :reminder.notification,
                'eta' :reminder.eta,
                'bale' :reminder.bale,
            })
        context = {
            'reminders': reminders,
        }
        return render(request, 'all_reminders.html', context)

    def post(self, request, *args, **kwargs):
        return render(request, 'all_reminders.html')


class AddReminder(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, *args, **kwargs):
        form = ReminderForm()
        context = {
            'form': form
            }
        return render(request, 'add_reminder.html', context)

    def post(self, request, *args, **kwargs):
        form = ReminderForm(request.POST)
        if form.is_valid():
            user = self.request.user
            title = request.POST.get('title')
            period = request.POST.get('period')
            active = True if request.POST.get('active') else False
            sms = True if request.POST.get('sms') else False
            email = True if request.POST.get('email') else False
            telegram = True if request.POST.get('telegram') else False
            date:str = request.POST.get('date')
            try:
                year, month, day = date.split('-')
            except:
                messages.error(request, 'تاریخ را به درستی وارد نکرده اید.')
                return render(request, 'add_reminder.html', {'form':form})
            time:str = request.POST.get('time')
            try:
                if ':' not in time:
                    hour = time
                    minute=0
                else:
                    hour, minute = time.split(':')
            except:
                messages.error(request, 'ساعت را به درستی وارد نکرده اید.')
                return render(request, 'add_reminder.html', {'form':form})
            try:
                jdt = jdatetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
                dt = jdt.togregorian()
            except:
                messages.error(request, 'زمان شروع یادآوری را به درستی مشخص نکرده اید. به ساختار نوشته شده در باکس ها دقت کنید.')
                return render(request, 'add_reminder.html', {'form':form})
            Reminder.objects.create(user=user, title=title, period=period, active=active, sms=sms, email=email, telegram=telegram, start_datetime=dt)
        else:
            messages.error(request, form.errors)
            return render(request, 'add_reminder.html', {'form':form})
        return redirect('all_reminders')


class UpdateReminder(LoginRequiredMixin, generic.UpdateView):
    model = Reminder

    def get(self, request, *args, **kwargs):
        obj:Reminder = self.get_object()
        form = ReminderForm(instance=obj)
        context = {
            'reminder': obj,
            'form': form,
            }
        return render(request, 'update_reminder.html', context)

    def post(self, request, *args, **kwargs):
        obj:Reminder = self.get_object()
        form = ReminderForm(request.POST, instance=obj)
        context = {
            'reminder': obj,
            'form': form,
            }
        if form.is_valid():
            title = request.POST.get('title')
            period = request.POST.get('period')
            active = True if request.POST.get('active') else False
            sms = True if request.POST.get('sms') else False
            email = True if request.POST.get('email') else False
            telegram = True if request.POST.get('telegram') else False
            date:str = request.POST.get('date')
            try:
                year, month, day = date.split('-')
            except:
                messages.error(request, 'تاریخ را به درستی وارد نکرده اید.')
                return render(request, 'update_reminder.html', context)
            time:str = request.POST.get('time')
            try:
                if ':' not in time:
                    hour = time
                    minute=0
                else:
                    hour, minute = time.split(':')
            except:
                messages.error(request, 'ساعت را به درستی وارد نکرده اید.')
                return render(request, 'update_reminder.html', context)
            try:
                jdt = jdatetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
                dt = jdt.togregorian()
            except:
                messages.error(request, 'زمان شروع یادآوری را به درستی مشخص نکرده اید. به ساختار نوشته شده در باکس ها دقت کنید.')
                return render(request, 'update_reminder.html', context)
            obj.title = title
            obj.period = period
            obj.active = active
            obj.sms = sms
            obj.email = email
            obj.telegram = telegram
            obj.start_datetime = dt
            obj.save()
        else:
            messages.error(request, form.errors)
            return render(request, 'update_reminder.html', context)
        return redirect('all_reminders')


class DeleteReminder(LoginRequiredMixin, generic.DeleteView):
    model = Reminder
    template_name = 'delete_reminder.html'

    def post(self, request, *args, **kwargs):
        reminder = self.get_object()
        reminder.delete()
        messages.success(self.request, 'یادآور %s با موفقیت حذف شد.' %reminder.title)
        return redirect('all_reminders')


def send_test_sms_for_madval(request):
    backend.send_s()
    return render(request, 'enter_number.html')


def send_test_email_for_madval(request):
    backend.send_e()
    return render(request, 'enter_number.html')


def send_test_telegram_message_for_madval(request):
    backend.send_t()
    return render(request, 'enter_number.html')
