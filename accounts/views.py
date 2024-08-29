from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model, login, logout
from django.db import IntegrityError, transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from requests.exceptions import ConnectTimeout, SSLError
import ghasedakpack
import random, string, time, threading

from config.madval1369_secret import *


sms = ghasedakpack.Ghasedak(GHASEDAK_API_KEY)
good_line_number_for_sending_otp = '30005088' # مال خودم رو که میذارم، شانسی از این شماره یا 20008580 میفرسته که شماره ۳۰۰۰ اوکی هست. ولی ۲۰۰۰ داغانه یه بار تقریبا ۲۰ دقیقه طول کشید تا بفرسته که خب دیگه یکبار رمز به درد بخوری نیست.


class EnterNumber(generic.TemplateView):
    template_name = 'enter_number.html'


class Login(generic.TemplateView):
    otps = dict()

    def get(self, request, *args, **kwargs):
        phone_number = request.GET.get('phone_number')
        if phone_number==None:
            messages.error(request, "لطفا شماره تلفن را وارد کنید.")
            return redirect('enter_number')
        if not phone_number.startswith('09'):
            messages.error(request, "لطفا شماره تلفن را با ۰۹ آغاز کنید.")
            return redirect('enter_number')
        if len(phone_number)!=11:
            messages.error(request, "لطفا شماره تلفن را به صورت ۱۱ رقمی وارد کنید و با ۰۹ آغاز کنید.")
            return redirect('enter_number')
        if phone_number.isalpha():
            messages.error(request, "در قسمتی از شماره تلفن، کاراکتری وجود دارد که عدد نیست.")
            return redirect('enter_number')
        if phone_number in Login.otps:
            messages.error(request, "یکبار رمز برای شما ارسال شده است. در صورتی که تا ۲ دقیقه دیگر به گوشی "
                           "شما نرسید، لطفا مجددا اقدام کنید.")
            return render(request, 'login.html', {'phone_number': phone_number})
        else:
            otp_type = request.GET.get('otp_type')
            otp = str(random.randint(100000, 999999))
            messages.success(request, f"یکبار رمز {otp}")
            Login.otps[phone_number]=otp
            try:
                # if otp_type=="sms":
                #     answer = sms.verification({'receptor': phone_number, 'linenumber': good_line_number_for_sending_otp,'type': '1', 'template': MY_TEMPLATE_NAME_IN_GHASEDAK_ME_SITE, 'param1': otp})
                # elif otp_type=="voice":
                #     answer = sms.verification({'receptor': phone_number, 'type': '2', 'template': MY_TEMPLATE_NAME_IN_GHASEDAK_ME_SITE_WITH_VOICE, 'param1': otp})
                answer = True
                if answer:
                    messages.success(request, "یکباررمز با موفقیت به شماره %s ارسال شد." %phone_number)
                    return render(request, 'login.html', {'phone_number': phone_number})
                else:
                    messages.error(request, "مشکلی در سرویس ارسال یکباررمز رخ داده است. لطفاً چند دقیقه بعد"
                                "مجددا تلاش کنید و یا از رمز ثابت خود استفاده کنید.")
                    return redirect('enter_number')
            except ConnectTimeout as error:
                messages.error(request, "مشکلی در سرویس ارسال یکباررمز رخ داده است. لطفاً چند دقیقه بعد"
                            "مجددا تلاش کنید و یا از رمز ثابت خود استفاده کنید.")
                messages.error(request, error)
                return redirect('enter_number')
            except SSLError as error:
                messages.error(request, "اروری مربوط به SSL رخ داده است. لطفاً از خاموش بودن VPN خود "
                               "مطمئن شوید و تنظیمات مربوط به پراکسی را نیز بررسی نمایید.")
                messages.error(request, error)
                return redirect('enter_number')
            except ConnectionError as error:
                messages.error(request, "مشکلی رخ داده است. لطفاً اتصال به اینترنت خود را بررسی کنید.")
                messages.error(request, error)
                return redirect('enter_number')
            finally:
                threading.Thread(target=self.expire_sent_otp, args=(phone_number, )).start()   

    def post(self, request, *args, **kwargs):
        phone_number = request.POST.get('phone_number')
        sent_otp = request.POST.get('otp')
        print(phone_number, sent_otp, type(phone_number), type(sent_otp))
        otps = Login.otps
        correct_otp = otps.get(phone_number)
        if correct_otp == None: # یعنی یا منقضی شده و یا طرف دستکاری کرده فرم رو با اچ تی ام ال
            messages.error(request, "یکباررمز منقضی شده است!")
            return redirect('enter_number')
        try:
            del Login.otps[phone_number]
        except: # ممکنه اکسپایر شده باشه یا نباشه تو دیکشنری یا به هر دلیلی. به هر حال میگم ارور نده. سعی کن پاکش کنی. شد شد نشد نشد ولش کن😁
            pass
        if correct_otp==sent_otp:
            user = get_user_model().objects.filter(username=phone_number).first()
            if user==None:
                user = get_user_model().objects.create(username=phone_number)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "خوش آمدی %s" %phone_number)
            return redirect('homepage')
        else:
            messages.error(request, "یکبار رمز به درستی وارد نشده است!")
            return redirect('enter_number')

    def expire_sent_otp(self, phone_number):
        time.sleep(120)
        try:
            del Login.otps[phone_number]
        except:
            pass


class Logout(generic.TemplateView):
    template_name = 'logout.html'

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('homepage')

