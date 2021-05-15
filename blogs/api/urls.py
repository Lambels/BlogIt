from django.urls import path
from .views import(
    like_dislike_blog_view,
    delete_subblog,
    delete_blog
)


app_name = 'blogs'


urlpatterns = [
    path('like_dislike_blog', like_dislike_blog_view, name='like_blog'),
    path('delete_subblog', delete_subblog, name='delete_subblog'),
    path('delete_blog', delete_blog, name='delete_blog')
]