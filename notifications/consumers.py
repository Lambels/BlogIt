from channels.generic.websocket import AsyncWebsocketConsumer
import json
from random import randint
import asyncio
import time
from .models import Notification
from channels.db import database_sync_to_async
from django.core import serializers


@database_sync_to_async
def get_notifications(user):
    notifications = Notification.objects.filter(userTo=user, seen=False, notified_about=False)
    if notifications.exists():
        for i in notifications:
            i.notified_about = True
            i.save()
        return serializers.serialize('json', notifications)
    return None


class NotificationConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        await self.accept()
        self.user = self.scope['user']


        while True:
            self.notifications = await get_notifications(self.user)
            if self.notifications:
                await self.send(json.dumps({'notifications': self.notifications}))
            await asyncio.sleep(3)


    async def disconnect(self):
        await self.close()