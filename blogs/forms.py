from django import forms
from .models import Blog, SubBlog, Tag
from django.contrib.auth.models import AnonymousUser


class CreateBlogForm(forms.ModelForm): 
    tags = forms.CharField(max_length=150,
            required=False,
            widget=forms.Textarea(
                attrs={
                    "placeholder": "Not Required",
                    "rows": 4,
                    "cols": 50,
                }
            ),
        )


    class Meta:
        model = Blog
        fields = ('title', 'snip', 'tags')


    def clean_title(self):
        if self.is_valid():
            title = self.cleaned_data['title']
            try:
                blog = Blog.objects.filter(author=self.instance.pk).get(title=title)
                raise forms.ValidationError('You already have a blog named %s' % title)
            except Blog.DoesNotExist:
                if '/' in title or '.' in title:
                    raise forms.ValidationError('Title cant contain symbols!')
                return title
    

    def clean_tags(self):
        if self.is_valid():
            tags = self.cleaned_data['tags'].split(", ")
            if len(tags) > 5:
                return forms.ValidationError('You cant have more then 5 tags!')
            return tags


    def save(self, commit=True):
        if self.is_valid():
            string_tags = self.cleaned_data['tags']
            title = self.cleaned_data['title']
            snip = self.cleaned_data['snip']
            blog = Blog(title=title, snip=snip, author=self.instance)
            blog.save()
            for tag_title in string_tags:
                tag = Tag.objects.get_or_create(name=tag_title.lower())
                blog.tags.add(tag[0])
            if commit:
                blog.save()
            return blog


class CreateSubBlogForm(forms.ModelForm):
    

    def __init__(self, user=AnonymousUser(), blog_pk=None, *args, **kwargs):
        super(CreateSubBlogForm, self).__init__(*args, **kwargs)
        self.user = user
        self.blog_pk = blog_pk


    class Meta:
        model = SubBlog
        fields = ('title', 'content')


    def clean_title(self):
        if self.is_valid():
            title = self.cleaned_data['title']
            try:
                SubBlog.objects.get(parent_blog=self.blog_pk, title=title)
                raise forms.ValidationError('You already have a sub blog named like this in this blog.')
            except SubBlog.DoesNotExist:
                if '/' in title or '.' in title:
                    raise forms.ValidationError('Title cant contain symbols.')
                return title


    def save(self, commit=True):
        if self.is_valid():
            if self.blog_pk:
                blog = Blog.objects.get(id=self.blog_pk)
                subblog = SubBlog.objects.create(
                    title=self.cleaned_data['title'],
                    parent_blog=blog,
                    content=self.cleaned_data['content'],
                )
                if commit:
                    subblog.save()
                return subblog
            


class UpdateBlogForm(forms.ModelForm):
    title = forms.CharField(max_length=15, required=False)
    snip = forms.CharField(max_length=20, required=False)
    tags = forms.CharField(required=False) 


    def __init__(self, blog=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blog = blog


    class Meta:
        model = Blog
        fields = ('title', 'snip', 'tags')


    def clean_title(self):
        if self.is_valid():
            title = self.cleaned_data['title']
            try:
                Blog.objects.get(author=self.instance.pk, title=title)
                raise forms.ValidationError("You already have a blog named like this.")
            except Blog.DoesNotExist:
                if '/' in title or '.' in title:
                    raise forms.ValidationError('Title cant contain symbols.')
                return title


    def clean_tags(self):
        if self.is_valid():
            tags = self.cleaned_data['tags'].split(", ")
            if len(tags) > 5:
                return forms.ValidationError('You cant have more then 5 tags!')
            return tags


    def save(self, commit=True):
        if self.is_valid():
            string_tags = self.cleaned_data['tags']
            title = self.cleaned_data['title']
            snip = self.cleaned_data['snip']
            self.blog.title = title
            self.blog.snip = snip
            self.blog.tags.clear()
            for tag_title in string_tags:
                tag = Tag.objects.get_or_create(name=tag_title.lower())
                self.blog.tags.add(tag[0])
            if commit:
                self.blog.save()
            return self.blog