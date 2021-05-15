from django.db import models
from users.models import Account


class Tag(models.Model):
    name = models.CharField(max_length=150)


    def __str__(self):
        return self.name
    


class Blog(models.Model):
    title               = models.CharField(max_length=15)
    author              = models.ForeignKey(Account, on_delete=models.CASCADE)
    tags                = models.ManyToManyField(Tag)
    snip                = models.CharField(max_length=20)
    likes               = models.IntegerField(default=0)
    added               = models.DateTimeField(auto_now_add=True)
    users_who_liked     = models.TextField()


    class Meta:
        ordering = ('-likes',)


    def like(self, user):
        self.likes += 1
        self.users_who_liked += f'/{user.username}'
        self.save(update_fields=['likes', 'users_who_liked'])
        from notifications.models import Notification
        try:
            Notification.objects.get(userTo=self.author, blog_obj=self, userWho=user)
        except Notification.DoesNotExist:
            if not user == self.author:
                Notification.objects.create(
                        userWho=user,
                        userTo=self.author,
                        acction='lk', 
                        blog_obj=self
                    )
        return self


    def dislike(self, user):
        if not user.username in self.users_who_liked:
            return models.BadRequest('You need to like first before you can dislike.')
        formated_username = f'/{user.username}'
        new_names = self.users_who_liked.replace(formated_username, '')
        self.users_who_liked = new_names
        self.likes -= 1
        self.save(update_fields=['likes', 'users_who_liked'])
        return self


    def __str__(self):
        return self.title
    


class SubBlog(models.Model):
    parent_blog         = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title               = models.CharField(max_length=15)
    content             = models.TextField()
    created_at          = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    