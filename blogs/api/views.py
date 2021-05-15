from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import LikeBlogSerializer, DeleteSubblogSerializer
from rest_framework.response import Response
from rest_framework import status
from users.models import Account
from rest_framework.authtoken.models import Token
from ..models import Blog


@api_view(['POST'])
@permission_classes([ IsAuthenticated, ])
def like_dislike_blog_view(request):


    if not request.POST:
        return Response({'message': 'You need to send a post request with arguments'}, status=status.HTTP_400_BAD_REQUEST)

    user = Token.objects.get(key=request.headers.get('Authorization')[6:]).user
    ctx = {'user': user}
    serializer = LikeBlogSerializer(user, data=request.POST, context=ctx)

    if serializer.is_valid():
        serializer.save()


        return Response({'message': 'Blog likes updated'}, status=status.HTTP_200_OK)


    return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([ IsAuthenticated, ])
def delete_subblog(request):


    if not request.POST:
        return Response({'message': 'You need to send a post request with arguments'}, status=status.HTTP_400_BAD_REQUEST)


    user = Token.objects.get(key=request.headers.get('Authorization')[6:]).user
    ctx = {'user': user}
    serializer = DeleteSubblogSerializer(user, data=request.POST, context=ctx)


    if serializer.is_valid():
        serializer.save()

        return Response({
            'message': 'Deleted blog.'
        }, status=status.HTTP_200_OK)

    return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([ IsAuthenticated, ])
def delete_blog(request):


    if not request.POST:
        return Response({'message': 'You need to send a post request with arguments'}, status=status.HTTP_400_BAD_REQUEST)


    blog = Blog.objects.filter(id=request.POST.get('blog_id', None))
    if not blog.exists():
        return Response({'message': 'Couldnt find blog'}, status=status.HTTP_400_BAD_REQUEST)
    if not blog[0].author == request.user:
        return Response({'message': 'Cant delete someone elses blog'}, status=status.HTTP_400_BAD_REQUEST)
    blog[0].delete()
    return Response({'message': 'Deleted Blog'}, status=status.HTTP_200_OK)