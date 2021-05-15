from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from .models import Blog, SubBlog
from users.models import Account
from random import shuffle
from .forms import CreateBlogForm, CreateSubBlogForm, UpdateBlogForm
from rest_framework.authtoken.models import Token


# Create your views here.
@require_http_methods(['GET'])
def user_blogs_view(request, name):
    ctx = {}


    if request.method == 'GET':

        requested_user = Account.objects.filter(username=name)[0]
        blogs          = Blog.objects.filter(author=requested_user)
        ctx['user']    = requested_user
        ctx['user_token'] = Token.objects.get(user=request.user).key
        
        if blogs.exists():

            for blog in blogs:
                subblogs = SubBlog.objects.filter(parent_blog=blog)
                if subblogs.exists():
                    ctx['subblogs'] = []
                    break

            try:
                ctx['subblogs']
                for blog in blogs:
                    subblogs = SubBlog.objects.filter(parent_blog=blog)
                    if subblogs.exists():
                        ctx['subblogs'].append({
                            blog.id: subblogs
                        })

            except KeyError:
                pass

            ctx['blogs'] = blogs

        if requested_user == request.user:

            
            return render(request, 'blogs/my-blogs.html', ctx)


        return render(request, 'blogs/user-blogs.html', ctx)


@require_http_methods(['GET'])
def blog_view(request, pk):
    ctx = {}


    if request.method == 'GET':

        requested_blog = get_object_or_404(Blog, id=pk)
        blog_owner = requested_blog.author
        subblogs = SubBlog.objects.filter(parent_blog=requested_blog)
        if subblogs.exists():
            ctx['subblogs'] = subblogs
        ctx['blog'] = requested_blog
        ctx['blog_owner'] = blog_owner


        if blog_owner == request.user:
            return render(request, 'blogs/my-blog.html', ctx)
        

        return render(request, 'blogs/user-blog.html', ctx)


def blog_query(user, query=None):
    
    if query == "":
        if not user.is_authenticated:
            results = list(Blog.objects.all())
            shuffle(results)
        else:
            unliked_results = list(Blog.objects.exclude(users_who_liked__contains=user.username))
            shuffle(unliked_results)
            liked_results = list(Blog.objects.filter(users_who_liked__contains=user.username))
            shuffle(liked_results)
            results = unliked_results + liked_results

    else:
        key_words = query.split(' ')
        for key_word in key_words:
            results = Blog.objects.filter(
                Q(tags__name__icontains=key_word) |
                Q(title__icontains=key_word) |
                Q(snip__icontains=key_word)
            ).distinct()


    return results


@require_http_methods(['GET'])
def confirm_delete(request, pk):
    ctx = {}
    if not request.user.is_authenticated:
        return redirect('home')
    blog = Blog.objects.filter(id=pk)
    if not blog.exists():
        return render(request, 'blogs/confirm_blog_delete.html')
    if blog[0].author == request.user:
        ctx['blog'] = blog[0]
        ctx['user_token'] = Token.objects.get(user=request.user).key
        return render(request, 'blogs/confirm_blog_delete.html', ctx)
    else:
        return redirect('home')


#Form Views
def add_blog_view(request):
    ctx = {}


    if not request.user.is_authenticated:
        return redirect('home')


    if request.POST:
        form = CreateBlogForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreateBlogForm()

    
    ctx['blog_form'] = form
    return render(request, 'blogs/add_blog.html', ctx)


def modify_blog_view(request, pk):
    ctx = {}


    if not request.user.is_authenticated:
        return redirect('home')

    
    blog = Blog.objects.get(id=pk)
    if not request.user == blog.author:
        return redirect('home')


    ctx['blog'] = blog
    ctx['user_token'] = Token.objects.get(user=request.user).key


    if request.GET:
        try:
            redirect_uri = request.GET.get('page')
            if redirect_uri == 'appearance':
                if request.POST:
                    form = UpdateBlogForm(blog, data=request.POST, instance=request.user)
                    if form.is_valid():
                        form.save()
                        ctx['success'] = True
                else:
                    form = UpdateBlogForm()
                ctx['blog_form'] = form
                return render(request, 'blogs/edit_blog_appearance.html', ctx)
            elif redirect_uri == 'content':
                if request.POST:
                    form = CreateSubBlogForm(request.user, blog.id, data=request.POST)
                    if form.is_valid():
                        form.save()
                else:
                    ctx['subblogs'] = SubBlog.objects.filter(parent_blog=blog)
                    form = UpdateBlogForm()
                ctx['blog_form'] = form
                return render(request, 'blogs/edit_blog_content.html', ctx)
            elif redirect_uri == 'important':
                return render(request, 'blogs/edit_blog_important.html', ctx)
        except KeyError:
            pass


        