from django.urls import path

from . import views


urlpatterns = [
    path('enter_number/', views.EnterNumber.as_view(), name='enter_number'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('rules/', views.Rules.as_view(), name='rules'),
    path('email/', views.Email.as_view(), name='email'),
    path('telegram/', views.Telegram.as_view(), name='telegram'),
]
