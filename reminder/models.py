from django.db import models
from django.contrib.auth import get_user_model


class Reminder(models.Model):
    EVERY_YEAR          = 'every year'
    EVERY_MONTH         = 'every month'
    EVERY_28_DAY        = 'every 28 day'
    EVERY_OTHER_WEEK    = 'every other week'
    EVERY_WEEK          = 'every week'
    EVERY_THIRD_DAY     = 'every third day'
    EVERY_OTHER_DAY     = 'every other day'
    EVERY_DAY           = 'every day'
    EVERY_12_HOUR       = 'every 12 hour'
    EVERY_8_HOUR        = 'every 8 hour'
    EVERY_6_HOUR        = 'every 6 hour'
    EVERY_4_HOUR        = 'every 4 hour'

    PERIOD_CHOICES = (
        (EVERY_YEAR, 'هر سال'),
        (EVERY_MONTH, 'هر ماه'),
        (EVERY_28_DAY, 'هر ۲۸ روز'),
        (EVERY_OTHER_WEEK, 'هر دو هفته'),
        (EVERY_WEEK, 'هر هفته'),
        (EVERY_THIRD_DAY, 'هر ۷۲ ساعت'),
        (EVERY_OTHER_DAY, 'هر ۴۸ ساعت'),
        (EVERY_DAY, 'هر روز'),
        (EVERY_12_HOUR, 'هر ۱۲ ساعت'),
        (EVERY_8_HOUR, 'هر ۸ ساعت'),
        (EVERY_6_HOUR, 'هر ۶ ساعت'),
        (EVERY_4_HOUR, 'هر ۴ ساعت'),
    )
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=64)
    start_datetime = models.DateTimeField()
    period = models.CharField(max_length=64, choices=PERIOD_CHOICES)
    active = models.BooleanField(default=True, verbose_name='فعال')
    sms = models.BooleanField(default=True, verbose_name='اس ام اس')
    email = models.BooleanField(default=False, verbose_name='ایمیل')
    notification = models.BooleanField(default=False, verbose_name='نوتیفیکیشن')
    telegram = models.BooleanField(default=False, verbose_name='تلگرام')
    whatsapp = models.BooleanField(default=False, verbose_name='واتساپ')
    eta = models.BooleanField(default=False, verbose_name='ایتا')
    bale = models.BooleanField(default=False, verbose_name='بله')

    def __str__(self):
        return self.title
