from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.urls import path, include
from home import views as homeviews
from users import views as userviews


urlpatterns = [
    path('admin/', admin.site.urls),


    #API URLS
    path('api/users/', include('users.api.urls')),
    path('api/blogs/', include('blogs.api.urls')),
    path('api/notifications/', include('notifications.api.urls')),


    #VIEW URLS
    path('', homeviews.home_screen_view, name='home'),
    path('logout/', userviews.logout_view, name='logout'),
    path('login/', userviews.login_view, name='login'),
    path('register/', userviews.register_view, name='register'),


    #USERS URLS
    path('user/', include('users.urls')),


    #BLOG URLS
    path('blog/', include('blogs.urls')),


    #NOTIFICATION URLS
    path('notifications/', include('notifications.urls')),


    #PASSWORD RESET URLS
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
    name='password_change_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),
]
