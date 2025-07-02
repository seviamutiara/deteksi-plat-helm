"""
WSGI config for PENGENALAN project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import mqtt.mqtt_handler
mqtt.mqtt_handler.run_mqtt_thread()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PENGENALAN.settings')

application = get_wsgi_application()
