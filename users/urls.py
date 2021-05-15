from django.urls import path
from .views import (
    user_view,
    account_update_form,
)


urlpatterns = [
    path('<str:name>', user_view, name="user"),
    path('account/configure', account_update_form, name="configure"),
]
