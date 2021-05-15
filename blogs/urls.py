from django.urls import path
from .views import (
    user_blogs_view,
    blog_view,
    add_blog_view,
    modify_blog_view,
    confirm_delete
)


urlpatterns = [
    path('user/<str:name>', user_blogs_view, name='userblogs'),
    path('view/<int:pk>', blog_view, name='blog_view'),
    path('compose', add_blog_view, name='create_blog'),
    path('update/<int:pk>', modify_blog_view, name='edit_blog'),
    path('delete/<int:pk>', confirm_delete, name='confirm_delete_blog')
]