from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	
from jalali_date import datetime2jalali, date2jalali
from django_madval.templatetags import madval_persian_translation as madval

from .models import Reminder

@admin.register(Reminder)
class ReminderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    model = Reminder
    list_display = ['user', 'title', 'get_jalali', 'period', 'active']
    list_display_links = ['user', 'title', 'get_jalali', 'period', 'active']
	
    @admin.display(description='تاریخ شروع')
    def get_jalali(self, obj):
        weekday = madval.persian_weekday(datetime2jalali(obj.start_datetime).strftime('%a'))
        month = madval.persian_month(datetime2jalali(obj.start_datetime).strftime('%b'))
        date_part1 = datetime2jalali(obj.start_datetime).strftime('%d')
        date_part2 = datetime2jalali(obj.start_datetime).strftime('%Y')
        hour = datetime2jalali(obj.start_datetime).strftime('%H:%M:%S')
        return madval.persian_numbers_int("%s %s %s %s ساعت %s" %(weekday, date_part1, month, date_part2, hour))