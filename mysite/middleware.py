from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from users.models import Account
from channels.middleware import BaseMiddleware
from rest_framework.authtoken.models import Token


#custom token auth middleware
@database_sync_to_async
def get_user(token):
    try:
        user = Token.objects.get(key=token).user
        return user
    except Account.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        token = scope['path'].split('/')[-1]
        scope['user'] = await get_user(token)
        return await super().__call__(scope, receive, send)