from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator

from .forms import PostForm, CommentForm, UserForm
from blog.models import Post, Category, User


def index(request):
    template = 'blog/index.html'
    posts = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    posts = get_object_or_404(
        Post,
        pk=id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )
    context = {'post': posts}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category_list = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = Post.objects.filter(
        category__slug=category_slug,
        is_published=True,
        pub_date__lte=timezone.now()
    )
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'post_list': page_obj, 'category': category_list}
    return render(request, template, context)


def get_posts(**kwargs):
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).annotate(comment_count=Count('comments')
               ).filter(**kwargs).order_by('-pub_date')


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', request.user)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


def profile(request, username):
    profile = get_object_or_404(
        User,
        username=username)
    posts = get_posts(author=profile)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    if request.user != profile:
        posts = get_posts(
            is_published=True,
            category__is_published=True,
            pub_date__lte=datetime.now(),
            author=profile)
    page_obj = paginator.get_page(page_number)
    context = {'profile': profile,
               'page_obj': page_obj}
    return render(request, 'blog/profile.html', context)
