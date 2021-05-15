from django.shortcuts import render
from .models import Notification
from rest_framework.authtoken.models import Token

# Create your views here.
def test(request):
    ctx = {}

    old_notifications = Notification.objects.filter(userTo=request.user, seen=True).order_by('-created_at')
    new_notifications = Notification.objects.filter(userTo=request.user, seen=False).order_by('-created_at')
    
    for notification in new_notifications:
        notification.seen = True
        notification.save()
    
    ctx['old_notifications'] = old_notifications
    ctx['new_notifications'] = new_notifications
    ctx['user_token']        = Token.objects.get(user=request.user).key

    
    return render(request, 'notifications/my_notifications.html', context=ctx)