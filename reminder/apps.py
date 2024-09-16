from django.apps import AppConfig
import threading

class ReminderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reminder'

    def ready(self):
        from .backend import send_sms_to_people
        threading.Thread(target=send_sms_to_people, daemon=True).start()
