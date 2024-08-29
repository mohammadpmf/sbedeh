
from threading import Thread
from time import sleep
from datetime import datetime, timezone

from requests.exceptions import ConnectTimeout, SSLError
import ghasedakpack

from .models import Reminder
from config.madval1369_secret import *


MINUTE = 60
sms = ghasedakpack.Ghasedak(GHASEDAK_API_KEY)

def sbede(phone_number, message, timeout_counter=0):
    if timeout_counter>=3:
        try:
            error_message = 'سلام از سایت sbede.ir.\n'\
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
            sbede(phone_number, message, timeout_counter+1)
    except ConnectTimeout as error:
        answer = sms.send({'message': message, 'receptor' : phone_number, 'linenumber': MY_LINE_NUMBER_ON_GHASEDAK_2})
        if answer:
            return
        sleep((timeout_counter+1)*MINUTE)
        sbede(phone_number, message, timeout_counter+1)
    except SSLError as error:
        if answer:
            return
        sleep((timeout_counter+1)*MINUTE)
        sbede(phone_number, message, timeout_counter+1)
    except ConnectionError as error:
        if answer:
            return
        sleep((timeout_counter+1)*MINUTE)
        sbede(phone_number, message, timeout_counter+1)


def handle_reminder(reminder: Reminder):
    phone_number = reminder.user
    message = reminder.title
    if reminder.sms:
        Thread(target=sbede, args=(phone_number, message+'\nلغو ۱۱'), daemon=True).start()


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
    # اگه کار کرد همه این پایینیا رو میتونم پاک کنم.
    if now.year<reminder_time.year:
        return False
    elif now.year>reminder_time.year:
        return True
    # اگه هیچ کودوم نبود سالشون مساویه
    if now.month<reminder_time.month:
        return False
    elif now.month>reminder_time.month:
        return True
    # اگه هیچ کودوم نبود ماهشون مساویه
    if now.day<reminder_time.day:
        return False
    elif now.day>reminder_time.day:
        return True
    # اگه هیچ کودوم نبود روزشون مساویه
    if now.hour<reminder_time.hour:
        return False
    elif now.hour>reminder_time.hour:
        return True
    # اگه هیچ کودوم نبود ساعتشون مساویه
    if now.minute<reminder_time.minute:
        return False
    elif now.minute>reminder_time.minute:
        return True
    # اگه هیچ کودوم نبود دقیقه شون مساویه
    # ثانیه هم لازم نیست چک کنیم. چون ۶۰ ثانیه یه بار داره رفرش میشه.
    # تو همین دقیقه اولین باری هست که یه ریمایندر اتفاق افتاده و باید
    # انجامش بدیم.
    return True
    # تو حالت های قبلی که ترو برمیگردوندیم، الان اتفاق نیفتاده. اما
    # از قبل شروع شده و باید بررسی کنیک که موعد تکرارش رسیده یا نه.


def should_i(now: datetime, start_datetime: datetime, period: str):
    '''
    تابعی که بررسی میکنه که آیا الان زمان ارسال پیام به کاربر رسیده یا نه
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
    sleep(MINUTE)
    send_sms_to_people()


Thread(target=send_sms_to_people, daemon=True).start()