from django.contrib import admin
from .models import Blog, SubBlog, Tag


# Register your models here.
admin.site.register(Blog)
admin.site.register(SubBlog)
admin.site.register(Tag)