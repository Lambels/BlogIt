from django.urls import path
from .consumers import NotificationConsumer


ws_urlpatterns = [
    path('ws/notifications/<str:name>', NotificationConsumer.as_asgi(), name="notification_consumer")
]