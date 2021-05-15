from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
from users.models import Account
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



class registration_view(APIView):
    serializer_class = RegistrationSerializer


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        return_value = {}
        if serializer.is_valid():
            account = serializer.save()
            return_value['response'] = 'succesfully registered an new account.'
            return_value['email']    = account.email 
            return_value['username'] = account.username
            token                    = Token.objects.get(user=account).key
            return_value['token']    = token
        else:
            return_value             = serializer.errors
        return Response(return_value)


