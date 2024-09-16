from threading import Thread
from time import sleep
from datetime import datetime

from requests.exceptions import ConnectTimeout, SSLError
import ghasedakpack
import telebot
import requests
import pytz

from .models import Reminder
from .email_handler import send_mail

from environs import Env

env = Env()
env.read_env()

MINUTE = 60
REFRESH_INTERVAL_SECONDS = 60
sms = ghasedakpack.Ghasedak(env('GHASEDAK_API_KEY'))


def send_s():
    try:
        sms.send({'message': 'تست روی سرور. لغو۱۱', 'receptor' : '09198004498', 'linenumber': env('MY_LINE_NUMBER_ON_GHASEDAK_1')})
    except:
        print('nashod s bedam.')


def send_t():
    try:
        now_utc = datetime.now(pytz.utc)
        iran_tz = pytz.timezone('Asia/Tehran')
        now_iran = now_utc.astimezone(iran_tz)
        bot = telebot.TeleBot(env('MY_TELEGRAM_BOT_API_TOKEN'))
        bot.send_message('84047486', now_iran)
        print('message sent successfully to', '84047486')
    except:
        print('nashod t bedam.')


def send_e():
    try:
        USERNAME = env('DJANGO_EMAIL_ADDRESS')
        PASSWORD = env('DJANGO_EMAIL_APP_PASSWORD')
        send_mail('sbedeh.ir', ['mohammad.pfallah@gmail.com'], 'تست ایمیل سرور', 'تست ایمیل سرور', server='smtp.gmail.com', username=USERNAME, password=PASSWORD)
    except:
        print('nashod e bedam.')


def sbedeh(phone_number, message, timeout_counter=0):
    if timeout_counter>=3:
        try:
            error_message = 'سلام از سایت sbedeh.ir.\n'\
            'متاسفانه در ارسال یکی از یادآوری های شما مشکلی رخ داده است.'\
            ' پس از ۳ بار تلاش، با مشکل مواجه شدیم. لطفاً به حساب کاربری خود مراجعه کنید تا یادآوری مربوطه '\
            'از خاطرتان نرود. با تشکر.\nلغو۱۱'
            answer = sms.send({'message': error_message, 'receptor' : phone_number, 'linenumber': env('MY_LINE_NUMBER_ON_GHASEDAK_1')})
            if answer:
                return
            else:
                answer = sms.send({'message': error_message, 'receptor' : phone_number, 'linenumber': env('MY_LINE_NUMBER_ON_GHASEDAK_2')})
                if answer:
                    return
                # نشد باید ببینم دیگه چه میشه کرد.
        except:
            answer = sms.send({'message': error_message, 'receptor' : phone_number, 'linenumber': env('MY_LINE_NUMBER_ON_GHASEDAK_2')})
            if answer:
                return
            # نشد باید ببینم دیگه چه میشه کرد.
        return
    try:
        answer = sms.send({'message': message, 'receptor' : phone_number, 'linenumber': env('MY_LINE_NUMBER_ON_GHASEDAK_1')})
        if answer:
            # yey 😊
            return
        else:
            answer = sms.send({'message': message, 'receptor' : phone_number, 'linenumber': env('MY_LINE_NUMBER_ON_GHASEDAK_2')})
            if answer:
                # yey 😁
                return
            sleep((timeout_counter+1)*MINUTE)
            sbedeh(phone_number, message, timeout_counter+1)
    except ConnectTimeout as error:
        answer = sms.send({'message': message, 'receptor' : phone_number, 'linenumber': env('MY_LINE_NUMBER_ON_GHASEDAK_2')})
        if answer:
            return
        sleep((timeout_counter+1)*MINUTE)
        sbedeh(phone_number, message, timeout_counter+1)
    except SSLError as error:
        answer = sms.send({'message': message, 'receptor' : phone_number, 'linenumber': env('MY_LINE_NUMBER_ON_GHASEDAK_2')})
        if answer:
            return
        sleep((timeout_counter+1)*MINUTE)
        sbedeh(phone_number, message, timeout_counter+1)
    except ConnectionError as error:
        answer = sms.send({'message': message, 'receptor' : phone_number, 'linenumber': env('MY_LINE_NUMBER_ON_GHASEDAK_2')})
        if answer:
            return
        sleep((timeout_counter+1)*MINUTE)
        sbedeh(phone_number, message, timeout_counter+1)


def tbedeh(chat_id, message):
    try:
        bot = telebot.TeleBot(env('MY_TELEGRAM_BOT_API_TOKEN'))
        bot.send_message(chat_id, message)
        print('message sent successfully to', chat_id)
    except telebot.apihelper.ApiTelegramException as error:
        print('-'*100, f'\n{error}\n', '-'*100, sep='')
    except requests.exceptions.ReadTimeout as error:
        print('-'*100, f'\n{error}\n', '-'*100, sep='')
    except requests.exceptions.ConnectTimeout as error:
        print('-'*100, f'\n{error}\n', '-'*100, sep='')
        print('-'*100,'\nFilter Shekan mikhad!!!\n','-'*100, sep='')


def ebedeh(email, message, timeout_counter=0):
    USERNAME = env('DJANGO_EMAIL_ADDRESS')
    PASSWORD = env('DJANGO_EMAIL_APP_PASSWORD')
    if timeout_counter<5:
        try:
            send_mail('sbedeh.ir', [email], 'یادآوری', message, server='smtp.gmail.com', username=USERNAME, password=PASSWORD)
            send_mail('sbedeh.ir', [email], 'یادآوری', message, server='smtp.gmail.com', username=USERNAME, password=PASSWORD)
        except:
            sleep(30)
            ebedeh(email, message, timeout_counter+1)
    elif timeout_counter<10:
        try:
            send_mail('sbedeh.ir', [email], 'یادآوری', message, server='smtp.gmail.com', username=USERNAME, password=PASSWORD)
        except:
            sleep(300)
            ebedeh(email, message, timeout_counter+1)
    elif timeout_counter<12:
        try:
            send_mail('sbedeh.ir', [email], 'یادآوری', message, server='smtp.gmail.com', username=USERNAME, password=PASSWORD)
        except:
            sleep(3600)
            ebedeh(email, message, timeout_counter+1)
    elif timeout_counter==13:
        try:
            fail_message = 'متاسفانه به دلیل نامشخصی، ارسال یادآوری به شما مشکل داشت. چندین بار سعی کردیم ایمیل با یادآوری مشخصی که تعیین کرده بودید را برایتان ارسال کنیم. اما متاسفانه پس از ۱۲ بار تلاش کردن در طی ۳ ساعت موفق به ارسال یادآوری شما نشدیم. این ایمیل جداگانه برای شما ارسال شده است جهت این که از طریق سایت sbedeh.ir یادآوری های خود را بازبینی کنید.\nموفق باشید.\nsbedeh.ir'
            send_mail('sbedeh.ir', [email], 'یادآوری', fail_message, server='smtp.gmail.com', username=USERNAME, password=PASSWORD)
        except:
            pass


def handle_reminder(reminder: Reminder):
    phone_number = reminder.user
    message = reminder.title
    if reminder.sms:
        Thread(target=sbedeh, args=(phone_number, message+'\nلغو ۱۱'), daemon=True).start()
    if reminder.telegram: # فیلتر شکن باید روشن باشه
        Thread(target=tbedeh, args=(reminder.user.telegram_chat_id, message), daemon=True).start()
    if reminder.email:
        Thread(target=ebedeh, args=(reminder.user.email, message), daemon=True).start()
        

def should_check(now: datetime, reminder_time: datetime):
    '''
    تابعی که بررسی میکنه که زمان بررسی کردن برای یه ریمایندر رسیده یا نه.
    اگه هنوز نرسیده باشه که فالس برمیگردونه و دیگه لازم نیست الکی وقتمون رو
    برای ادامه بررسی ها بذاریم. اما اگه همین الان زمانش باشه یا از زمانش گذشته
    باشه و این بار دفعه دوم یا بیشتر باشه و به هر حال نیاز به بررسی داشته باشه
    ترو برمیگردونه.
    '''
    if now<reminder_time:
        return False
    return True
    

def should_i(now: datetime, start_datetime: datetime, period: str):
    '''
    تابعی که بررسی میکنه که آیا در این دقیقه زمان ارسال پیام به کاربر رسیده یا نه
    '''
    difference = now - start_datetime # اول قدر مطلق گرفتم. ولی لازم نیست. چون قبلش یه مرحله چک کردیم
    difference_in_minutes = difference.seconds // MINUTE
    # برای سال و ماه فرق داره و نمیشه مثل پایینی ها بررسی کرد.
    # چون سال کبیسه هم داریم و ماهی هم که تو کبیسه تغییر میکنه فرق داره.
    # اما ۲۸ روز یک بار یا ۱۴ روز یک بار یا هر چیز دیگه ای، اینا رو با تفاوت
    # دقیقه و ساعت میشه حساب کرد. اما این کار روی سال و ماه مشکل ایجاد میکرد.
    # به خاطر همین ساختار اینا فرق داره با اونا.
    if period==Reminder.EVERY_YEAR:
        if now.month!=start_datetime.month:
            return False
        if now.day!=start_datetime.day:
            return False
        if now.hour!=start_datetime.hour:
            return False
        if now.minute!=start_datetime.minute:
            return False
        return True
    elif period==Reminder.EVERY_MONTH:
        if now.day!=start_datetime.day:
            return False
        if now.hour!=start_datetime.hour:
            return False
        if now.minute!=start_datetime.minute:
            return False
        return True
    elif period==Reminder.EVERY_28_DAY:
        return difference_in_minutes%(672*MINUTE)==0
    elif period==Reminder.EVERY_OTHER_WEEK:
        return difference_in_minutes%(336*MINUTE)==0
    elif period==Reminder.EVERY_WEEK:
        return difference_in_minutes%(168*MINUTE)==0
    elif period==Reminder.EVERY_THIRD_DAY:
        return difference_in_minutes%(72*MINUTE)==0
    elif period==Reminder.EVERY_OTHER_DAY:
        return difference_in_minutes%(48*MINUTE)==0
    elif period==Reminder.EVERY_DAY:
        return difference_in_minutes%(24*MINUTE)==0
    elif period==Reminder.EVERY_12_HOUR:
        return difference_in_minutes%(12*MINUTE)==0
    elif period==Reminder.EVERY_8_HOUR:
        return difference_in_minutes%(8*MINUTE)==0
    elif period==Reminder.EVERY_6_HOUR:
        return difference_in_minutes%(6*MINUTE)==0
    elif period==Reminder.EVERY_4_HOUR:
        return difference_in_minutes%(4*MINUTE)==0


def send_sms_to_people():
    while True:
        bot = telebot.TeleBot(env('MY_TELEGRAM_BOT_API_TOKEN'))
        now_utc = datetime.now(pytz.utc)
        iran_tz = pytz.timezone('Asia/Tehran')
        now_iran = now_utc.astimezone(iran_tz)
        bot.send_message('84047486', now_iran)
        reminders = Reminder.objects.filter(active=True).select_related('user')
        for reminder in reminders:
            if should_check(now_iran, reminder.start_datetime):
                if should_i(now_iran, reminder.start_datetime, reminder.period):
                    handle_reminder(reminder)
                # bot.send_message('84047486', reminder.start_datetime)
        sleep(REFRESH_INTERVAL_SECONDS)
