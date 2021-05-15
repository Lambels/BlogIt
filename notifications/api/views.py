from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import DeleteNotificationSerializer
from rest_framework.response import Response
from rest_framework import status
from users.models import Account
from rest_framework.authtoken.models import Token


@api_view(['POST'])
@permission_classes([ IsAuthenticated, ])
def delete_notification_view(request):
    ctx = {}

    if not request.POST:
        return Response({'message': 'You need to send a post request with arguments'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = Token.objects.get(key=request.headers.get('Authorization')[6:]).user
    ctx = {'user': user}
    serialzier = DeleteNotificationSerializer(user, data=request.POST, context=ctx)

    if serialzier.is_valid():
        serialzier.save()


        return Response({'message': 'Notification Delted.'}, status=status.HTTP_200_OK)


    return Response({'message': serialzier.errors}, status=status.HTTP_400_BAD_REQUEST)