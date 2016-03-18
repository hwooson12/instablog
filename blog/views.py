from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import PermissionDenied

from .models import Post, Category, Comment, Sentiword
from .forms import PostForm
from .forms import PostEditForm

from konlpy.tag import Mecab


def hello(request):
    return HttpResponse('hello world')


def hello_with_tem(request):
    return render(request, 'hello.html')


def list_posts(request):
    per_page = 5
    current_page = request.GET.get('page', 1)

    # when A model is related to B model and data A are gotten from B model,
    # data on B model are come with data A.
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
    the_comment = Comment.objects.filter(post=the_post)
    mecab = Mecab()
    morph = mecab.pos(the_post.content)
    the_morph = ' '.join(str(e) for e in morph)



    if request.method == 'GET':
        pass
    elif request.method =='POST':
        new_comment = Comment()
        new_comment.content = request.POST.get('content')
        new_comment.post = the_post
        new_comment.save()




    return render(request, 'view_post.html',{
        'post' : the_post,
        'comments' : the_comment,
        'morph' : the_morph,
    })

def learning(request, pk):
    the_post = get_object_or_404(Post, pk=pk)
    mecab = Mecab()
    morph = mecab.pos(the_post.content)


    if request.method=="GET":
        pass
    elif request.method=="POST" and the_post.sentiword_set.exists()==False:
        for m in range(len(morph)):
            the_word = Sentiword()
            the_word.word = str(morph[m])
            the_word.post = the_post
            the_post.senti = request.POST.get('senti')
            the_post.save()
            the_word.save()
        return redirect('view_post', pk=pk)
    else:
        return redirect('view_post', pk=pk)

    return render(request, 'learning.html',{
        'post':the_post,
    })


# this pattern is often used in django.
@login_required
def create_post(request):
    categories = Category.objects.all()
    if request.method == 'GET':
        form = PostEditForm()
    elif request.method == "POST":
        form = PostEditForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            # new_post = Post()
            # new_post.title = form.cleaned_data['title']
            # new_post.content = form.cleaned_data['content']
            #
            # category_pk = request.POST.get('category')
            # category = get_object_or_404(Category, pk=category_pk)
            # new_post.categories = category
            # new_post.save()

            return redirect('view_post', pk=new_post.pk)

    return render(request, 'create_post.html',{
        'categories' : categories,
        'form' : form,

    })
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method =='GET':
        post = get_object_or_404(Post, pk=pk)
        categories = Category.objects.all()
    else:
        form = request.POST
        category = get_object_or_404(Category, pk=form['category'])
        post.title = form['title']
        post.content = form['content']
        post.category = category
        post.save()
        return redirect('view_post', pk=post.pk)
    return render(request,'edit.html',{
        'post':post,
        'categories':categories,
    })

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        post.delete()
        return redirect('list_posts')

    return render(request, 'delete.html',{
        'post':post,
    })
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method =='POST':
        comment.delete()
        return redirect('view_post', pk=comment.post.pk)

    return render(request, 'delete_comment.html',{
        'comment':comment,
    })
