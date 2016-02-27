from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from .models import Post
from .models import Category


def hello(request):
    return HttpResponse('hello world')


def hello_with_tem(request):
    return render(request, 'hello.html')


def list_posts(request):
    per_page = 5
    current_page = request.GET.get('page', 1)

    all_posts = Post.objects.\
        select_related().\
        prefetch_related().\
        all().\
        order_by('-pk')

    pagi = Paginator(all_posts, per_page)

    try:
        pg = pagi.page(current_page)
    except PageNotAnInteger:
        pg = pagi.page(1)
    except EmptyPage:
        pg = []


    return render(request, 'list_posts.html', {
        'posts' : pg,
    })

def view_post(request, pk):
    the_post = get_object_or_404(Post, pk=pk)

    return render(request, 'view_post.html',{
        'post' : the_post,
    })

def create_post(request):
    categories = Category.objects.all()
    if request.method == 'GET':
        pass
    elif request.method == "POST":
        new_post = Post()
        new_post.title = request.POST.get('title')
        new_post.content = request.POST.get('content')

        category_pk = request.POST.get('category')
        category = get_object_or_404(Category, pk=category_pk)
        new_post.categories = category
        new_post.save()

        return redirect('view_post', pk=new_post.pk)

    return render(request, 'create_post.html',{
        'categories' : categories,
    })