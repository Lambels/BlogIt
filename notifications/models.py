from django.db import models
from users.models import Account
from blogs.models import Blog


class Notification(models.Model):


    CHOICES = (
        ('lk', 'like'),
        ('fl', 'follow'),
    )


    userWho             = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='userWhoDidTheAction')
    userTo              = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='userTwordsWhoTheActionIsDirected')
    acction             = models.CharField(max_length=2)
    created_at          = models.DateTimeField(auto_now_add=True)
    account_obj         = models.ForeignKey(Account, blank=True, null=True, on_delete=models.CASCADE)
    blog_obj            = models.ForeignKey(Blog, blank=True, null=True, on_delete=models.CASCADE)
    seen                = models.BooleanField(default=False)
    notified_about      = models.BooleanField(default=False)