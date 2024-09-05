from django.urls import path

from . import views


urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('all_reminders/', views.AllReminders.as_view(), name='all_reminders'),
    path('add_reminder/', views.AddReminder.as_view(), name='add_reminder'),
    path('update/<int:pk>/', views.UpdateReminder.as_view(), name='update_reminder'),
    path('delete/<int:pk>/', views.DeleteReminder.as_view(), name='delete_reminder'),
]
