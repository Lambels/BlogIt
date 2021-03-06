# Generated by Django 3.2 on 2021-04-28 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blogs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acction', models.CharField(max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('notified_about', models.BooleanField(default=False)),
                ('account_obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('blog_obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogs.blog')),
                ('userTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userTwordsWhoTheActionIsDirected', to=settings.AUTH_USER_MODEL)),
                ('userWho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userWhoDidTheAction', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
