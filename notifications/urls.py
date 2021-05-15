from django.urls import path
from .views import (
    test
)


urlpatterns = [
    path('', test, name="notifications"),
]