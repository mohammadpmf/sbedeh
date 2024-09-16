from django.contrib.auth import get_user_model

from threading import Thread
from time import sleep
from datetime import datetime, timezone

from requests.exceptions import ConnectTimeout, SSLError
import ghasedakpack
import telebot
import requests

from .models import Reminder
from .email_handler import send_mail
from config.madval1369_secret import *


MINUTE = 60
REFRESH_INTERVAL_SECONDS = 60
PROXIES = {
    'http': 'http://your_proxy_address:port',
    'https': 'https://your_proxy_address:port',
}

sms = ghasedakpack.Ghasedak(GHASEDAK_API_KEY)


def send_s():
    try:
        sms.send({'message': 'تست روی سرور. لغو۱۱', 'receptor' : '09198004498', 'linenumber': MY_LINE_NUMBER_ON_GHASEDAK_1})
    except:
        print('nashod s bedam.')


def send_t():
    try:
        bot = telebot.TeleBot(MY_TELEGRAM_BOT_API_TOKEN)
        bot.send_message('84047486', 'تست روی سرور تلگرام')
        print('message sent successfully to', '84047486')
    except:
        print('nashod t bedam.')


def send_e():
    try:
        USERNAME = DJANGO_EMAIL_ADDRESS
        PASSWORD = DJANGO_EMAIL_APP_PASSWORD
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
            answer = sms.send({'message': error_message, 'receptor' : phone_number, 'linenumber': MY_LINE_NUMBER_ON_GHASEDAK_1})
            if answer:
                return
            else:
                answer = sms.send({'message': error_message, 'receptor' : phone_number, 'linenumber': MY_LINE_NUMBER_ON_GHASEDAK_2})
                if answer:
                    return
                # نشد باید ببینم دیگه چه میشه کرد.
        except:
            answer = sms.send({'message': error_message, 'receptor' : phone_number, 'linenumber': MY_LINE_NUMBER_ON_GHASEDAK_2})
            if answer:
                return
            # نشد باید ببینم دیگه چه میشه کرد.
        return
    try:
        answer = sms.send({'message': message, 'receptor' : phone_number, 'linenumber': MY_LINE_NUMBER_ON_GHASEDAK_1})
        if answer:
            # yey 😊
            return
        else:
            answer = sms.send({'message': message, 'receptor' : phone_number, 'linenumber': MY_LINE_NUMBER_ON_GHASEDAK_2})
            if answer:
                # yey 😁
                return
            sleep((timeout_counter+1)*MINUTE)
            sbedeh(phone_number, message, timeout_counter+1)
    except ConnectTimeout as error:
        answer = sms.send({'message': message, 'receptor' : phone_number, 'linenumber': MY_LINE_NUMBER_ON_GHASEDAK_2})
        if answer:
            return
        sleep((timeout_counter+1)*MINUTE)
        sbedeh(phone_number, message, timeout_counter+1)
    except SSLError as error:
        answer = sms.send({'message': message, 'receptor' : phone_number, 'linenumber': MY_LINE_NUMBER_ON_GHASEDAK_2})
        if answer:
            return
        sleep((timeout_counter+1)*MINUTE)
        sbedeh(phone_number, message, timeout_counter+1)
    except ConnectionError as error:
        answer = sms.send({'message': message, 'receptor' : phone_number, 'linenumber': MY_LINE_NUMBER_ON_GHASEDAK_2})
        if answer:
            return
        sleep((timeout_counter+1)*MINUTE)
        sbedeh(phone_number, message, timeout_counter+1)


def tbedeh(chat_id, message):
    try:
        bot = telebot.TeleBot(MY_TELEGRAM_BOT_API_TOKEN)
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
    USERNAME = DJANGO_EMAIL_ADDRESS
    PASSWORD = DJANGO_EMAIL_APP_PASSWORD
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
    now = datetime.now().replace(tzinfo=timezone.utc)
    reminders = Reminder.objects.filter(active=True).select_related('user')
    for reminder in reminders:
        if should_check(now, reminder.start_datetime):
            if should_i(now, reminder.start_datetime, reminder.period):
                handle_reminder(reminder)
    sleep(REFRESH_INTERVAL_SECONDS)
    send_sms_to_people()


# با فیلترشکن کار میکنه.
def activate_telegram_bot():
    global bot
    bot = telebot.TeleBot(MY_TELEGRAM_BOT_API_TOKEN)

    @bot.message_handler(commands=['start', 'help', 'ok']) # لیست دستوراتی که با اسلش کار میکنند. /start /help /ok
    def send_start(message):
        bot.reply_to(message, "به ربات تلگرامی سایت sbedeh.ir خوش آمدید🌺\n"
                    "برای ذخیره شدن حساب کاربری خود جهت دریافت پیام از طریق تلگرام، ابتدا شماره "
                    "ثبت نامی خود و سپس چت آی دی تلگرام خود را با یک فاصله از هم وارد کنید.\n"
                    "به طور مثال 09123456789 35682496\n"
        "(دقت کنید در صورت ارسال اشتباه چت آی دی، پیام ها برای شما ارسال نمی شوند.)")


    @bot.message_handler(func=lambda message: True) # لیست دستوراتی که مستقیم در چت مینویسیم.
    def handle_message(message):
        text:str = message.text.lower()
        if text==None:
            bot.reply_to(message, "لطفا شماره ثبت نامی خود و چت آی دی تلگرام خود را با یک فاصله از هم وارد کنید.")
            return
        two_texts = text.split(' ')
        if len(two_texts)<2:
            bot.reply_to(message, "فرمت خواسته شده را رعایت نکردید. لطفا شماره ثبت نامی خود "
                         "و چت آی دی تلگرام خود را با یک فاصله از هم وارد کنید. (شما هیچ فاصله ای "
                         "وارد نکرده‌اید!)")
            return
        if len(two_texts)>2:
            bot.reply_to(message, "فرمت خواسته شده را رعایت نکردید. لطفا شماره ثبت نامی خود "
                         "و چت آی دی تلگرام خود را با یک فاصله از هم وارد کنید. (شما بیش از یک فاصله "
                         "وارد کرده‌اید!)")
            return
        number, chat_id = two_texts[0].strip(), two_texts[1].strip()
        if not number.startswith('09'):
            bot.reply_to(message, "شماره با 09 آغاز نشده است!")
        elif len(number)!=11:
            bot.reply_to(message, "شماره باید ۱۱ رقمی باشد و با 09 آغاز شود!")
        elif not number.isdigit():
            bot.reply_to(message, "در قسمتی از شماره تلفن، کاراکتری وجود دارد که عدد نیست. شماره باید ۱۱ رقمی و با کیبورد انگلیسی وارد شود و با 09 آغاز شود!")
        elif not chat_id.isdigit():
            bot.reply_to(message, "در قسمتی از چت آی دی، کاراکتری وجود دارد که عدد نیست. چت آی دی باید با کیبورد انگلیسی وارد شود!")
        else:
            user = get_user_model().objects.filter(username=number).first()
            if not user:
                bot.reply_to(message, "شماره ارسالی در سایت پیدا نشد. جهت استفاده از این ربات ابتدا باید با شماره ای که ارسال کردید در سایت www.sbedeh.ir ثبت نام کنید.")
            else:
                user.telegram_chat_id=chat_id
                user.save()
                bot.reply_to(message, "شماره شما (%s) در سایت پیدا شد و جهت دریافت پیام از "
                            "چت آی دی تلگرامی ارسال شده (%s) استفاده خواهد شد.\n"
                            "در صورت نیاز به تغییر شماره تلگرامی که پیام ها را دریافت کند، "
                            "می توانید از حساب کاربری مورد نظر به این ربات پیام ارسال کنید و با وارد کردن "
                            "مجدد شماره و چت آی دی خود، اکانتی که پیام را دریافت می کند بروزرسانی کنید.\n"
                            "با تشکر\n www.sbedeh.ir" %(number, chat_id))
    bot.infinity_polling()

Thread(target=send_sms_to_people, daemon=True).start()
