from django.shortcuts import render
from users.models import Account
from blogs.views import blog_query
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator
from notifications.models import Notification



def home_screen_view(request):
    ctx = {}

    query = ''
    page_number = 1

    if request.GET:
        if request.GET.get('q'):
            query = request.GET['q']
            ctx['query']  = str(query)
        if request.GET.get('page'):
            page_number = request.GET.get('page')

            
    if request.user.is_authenticated:
        user_token = Token.objects.get(user=request.user)
        ctx['user_token'] = user_token
        notifications = Notification.objects.filter(userTo=request.user, seen=False)
        if notifications.exists():
            ctx['notifications'] = notifications

        
    blog_posts = blog_query(request.user, query)
    book_paginator = Paginator(blog_posts, 10)
    page = book_paginator.get_page(page_number)
    ctx['page'] = page


    return render(request, 'home/home.html', ctx)