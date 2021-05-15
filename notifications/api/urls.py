from django.urls import path
from .views import(
    delete_notification_view
)


app_name = 'notifications'


urlpatterns = [
    path('delete_notification', delete_notification_view, name='delete_notification'),
]