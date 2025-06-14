from django.apps import AppConfig
import threading
import sys

class AkunConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'akun'

    def ready(self):
        if 'runserver' in sys.argv:
            from mqtt import mqtt_handler
            mqtt_thread = threading.Thread(target=mqtt_handler.start_mqtt)
            mqtt_thread.daemon = True
            mqtt_thread.start()