# Generated by Django 5.1 on 2024-08-29 10:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('start_datetime', models.DateTimeField()),
                ('period', models.CharField(choices=[('every year', 'هر سال'), ('every month', 'هر ماه'), ('every 28 day', 'هر ۲۸ روز'), ('every other week', 'هر دو هفته'), ('every week', 'هر هفته'), ('every third day', 'هر ۷۲ ساعت'), ('every other day', 'هر ۴۸ ساعت'), ('every day', 'هر روز'), ('every 12 hour', 'هر ۱۲ ساعت'), ('every 8 hour', 'هر ۸ ساعت'), ('every 6 hour', 'هر ۶ ساعت'), ('every 4 hour', 'هر ۴ ساعت')], max_length=64)),
                ('active', models.BooleanField(default=True, verbose_name='فعال')),
                ('sms', models.BooleanField(default=True, verbose_name='اس ام اس')),
                ('email', models.BooleanField(default=False, verbose_name='ایمیل')),
                ('notification', models.BooleanField(default=False, verbose_name='نوتیفیکیشن')),
                ('telegram', models.BooleanField(default=False, verbose_name='تلگرام')),
                ('whatsapp', models.BooleanField(default=False, verbose_name='واتساپ')),
                ('eta', models.BooleanField(default=False, verbose_name='ایتا')),
                ('bale', models.BooleanField(default=False, verbose_name='بله')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reminders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
