from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, AuthenticationForm, AccountUpdateForm
from .models import Account
from rest_framework.authtoken.models import Token
from blogs.models import Blog


# Create your views here.
def register_view(request):
    ctx = {}
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email        = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account      = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            ctx['registration_form'] = form
    else:
        form = RegisterForm()
        ctx['registration_form'] = form
    return render(request, 'users/register.html', ctx)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    ctx = {}


    user = request.user
    if user.is_authenticated:
        return redirect('home')


    if request.POST:
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            email      = request.POST['email']
            password   = request.POST['password']
            user       = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    ctx['login_form'] = form
    return render(request, 'users/login.html', ctx)


@require_http_methods(["GET"])
def user_view(request, name):
    ctx = {}
    if request.user.is_authenticated:
        user_token = Token.objects.get(user=request.user)
        ctx['user_token'] = user_token
    if request.method == "GET":
        requested_user = Account.objects.filter(username=name)
        current_user = request.user
        if requested_user.exists():
            users_blogs = Blog.objects.filter(author=requested_user[0]).order_by('-added')
            ctx['user'] = requested_user[0]
            if users_blogs.exists():
                ctx['users_blogs'] = users_blogs[:3]
                ctx['most_liked_blog'] = users_blogs.order_by('-likes')[0]
            if requested_user[0] == current_user:
                return render(request, 'users/me.html', ctx)
        else:
            return render(request, 'users/not-found.html', ctx)
            
    return render(request, 'users/user.html', ctx)


def account_update_form(request):
    

    ctx = {}


    if not request.user.is_authenticated:
        return redirect('home')


    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = AccountUpdateForm(
            initial={
                'username': request.user.username,
                'description': request.user.description,
            }
        )


    ctx['account_form'] = form
    return render(request, 'users/configure-user.html', ctx)