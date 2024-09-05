from django import forms

from .models import Reminder

class ReminderFormToSHow(forms.Form):
    active = forms.BooleanField(disabled=True)
    sms = forms.BooleanField(disabled=True)
    email = forms.BooleanField(disabled=True)
    telegram = forms.BooleanField(disabled=True)
    whatsapp = forms.BooleanField(disabled=True)
    notification = forms.BooleanField(disabled=True)
    eta = forms.BooleanField(disabled=True)
    bale = forms.BooleanField(disabled=True)


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'period', 'active', 'sms', 'email', 'telegram']

    title = forms.CharField(max_length=64, label='عنوان یادآوری')
    # start_datetime = forms.DateTimeField(label='', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    period = forms.TypedChoiceField(choices=Reminder.PERIOD_CHOICES, label='دوره چرخش یادآوری', widget=forms.Select(attrs={'style': 'height: 40px;'}))
    active = forms.BooleanField(required=False, initial=True, help_text='در صورت غیر فعال کردن یک یادآوری، پیامی از طرف سایت sbedeh.ir برای شما ارسال نخواهد شد.', label='فعال بودن این یادآوری')
    sms = forms.BooleanField(required=False, initial=True, help_text='جهت دریافت اس ام اس، دقت کنید که شماره های تبلیغاتی را مسدود نکرده باشید. در غیر این صورت اس ام اس های ارسالی به شما مسدود خواهند شد.', label='ارسال اس ام اس')
    email = forms.BooleanField(required=False, initial=True, help_text='جهت دریافت پیام از طریق ایمیل، باید از قسمت تنظیمات سایت آدرس ایمیل معتبر خود را وارد کنید.', label='ارسال ایمیل')
    telegram = forms.BooleanField(required=False, initial=True, help_text='جهت دریافت پیغام از طریق تلگرام، باید از قسمت تنظیمات سایت، chat_id تلگرامی خود را اضافه کنید و یک پیغام از اکانت مورد نظر برای ربات تلگرامی با آی دی @sbedeh_bot ارسال کنید تا ربات تلگرامی توانایی ارسال پیغام برای شما را داشته باشد.', label='ارسال پیام در تلگرام')
    # whatsapp = forms.BooleanField(disabled=True, help_text='در حال حاضر فعال نیست', label='واتساپ')
    # notification = forms.BooleanField(disabled=True, help_text='در حال حاضر فعال نیست', label='نوتیفیکیشن')
    # eta = forms.BooleanField(disabled=True, help_text='در حال حاضر فعال نیست', label='ایتا')
    # bale = forms.BooleanField(disabled=True, help_text='در حال حاضر فعال نیست', label='بله')
