from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from forum.forms import LoginForm
from forum.forms import RegisterForm
from forum.forms import ProfileForm
from forum.forms import ProfileChangeForm
from forum.forms import NewContentForm
from forum.forms import SearchForm
from forum.models import ForumUser
from forum.models import Category
from forum.models import Topic
from forum.models import Post


def index(request):
    main_category = Category.objects.get(title='Main')
    is_special = request.user.groups.filter(name="SpecialUser").exists()

    return render(request, 'index.html', locals())


def make_paginator(request, objects, num_items):
    paginator = Paginator(objects, num_items)
    page = request.GET.get('page')
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    return result


def category_view(request, category_id):
    topics = Topic.objects.filter(category_id=category_id).order_by(
        '-last_modified')
    topics = make_paginator(request, topics, 20)
    category = get_object_or_404(Category, pk=category_id)

    return render(request, 'category.html', locals())


def topic_view(request, topic_id):
    posts = Post.objects.filter(topic_id=topic_id).order_by('created_at')
    posts = make_paginator(request, posts, 3)
    topic = get_object_or_404(Topic, pk=topic_id)

    return render(request, 'topic.html', locals())


@login_required(login_url="/fothon/login")
def new_content_view(request, content_type, content_id):
    if content_type not in ('topic', 'post'):
        return redirect('/fothon')
    if request.method == 'POST':
        form = NewContentForm(request.POST)
        if form.is_valid():
            content = request.POST['content']
            user = get_object_or_404(ForumUser,
                                     username=request.user.username)
            if content_type == 'topic':
                Topic.objects.create(title=content, category_id=content_id,
                                     author=user, last_modified_from=user)
            elif content_type == 'post':
                post = Post.objects.create(text=content, topic_id=content_id,
                                           author=user)
                topic = get_object_or_404(Topic, pk=content_id)
                topic.last_modified = post.created_at
                topic.last_modified_from = post.author
                topic.save()
            return redirect(request.REQUEST['back'])
    else:
        form = NewContentForm()

    return render(request, 'new_content.html', locals())


def login_view(request):
    if request.user.is_authenticated():
        return redirect('/fothon')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect('/fothon')
            else:
                return HttpResponse("You are not logged in!")
    else:
        form = LoginForm()

    return render(request, 'login.html', locals())


def register_view(request):
    if request.user.is_authenticated():
        return redirect('/fothon')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            user_by_username = ForumUser.objects.filter(username=username)
            user_by_email = ForumUser.objects.filter(email=email)
            if not (user_by_username or user_by_email):
                user = ForumUser.objects.create_user(username, email,
                                                     password)
                return redirect('/fothon')
            else:
                return HttpResponse("Your username or email already exists!")
    else:
        form = RegisterForm()

    return render(request, 'register.html', locals())


@login_required(login_url="/fothon/login")
def logout_view(request):
    logout(request)
    return redirect('/fothon')


@login_required(login_url="/fothon/login")
def profile_change_view(request):
    user = get_object_or_404(ForumUser, username=request.user.username)
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST)
        if form.is_valid():
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.gender = request.POST['gender']
            user.city = request.POST['city']
            if request.POST['birth_date']:
                user.birth_date = request.POST['birth_date']
            user.save()
            return redirect('/fothon/profile')
    else:
        form = ProfileChangeForm(instance=user)

    return render(request, 'profile_change.html', locals())


@login_required(login_url="/fothon/login")
def profile_view(request, username=None):
    if not username:
        user = get_object_or_404(ForumUser, username=request.user.username)
    else:
        user = get_object_or_404(ForumUser, username=username)

    return render(request, 'profile.html', locals())


def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = request.POST['search_field']
            type = request.POST['type']
            search_result = []
            if type == 'post':
                search_result = Post.objects.filter(
                    text__icontains=search_text)
            elif type == 'topic':
                search_result = Topic.objects.filter(
                    title__contains=search_text)
            elif type == 'category':
                search_result = Category.objects.filter(
                    title__contains=search_text)

            if type != 'category':
                if request.POST['author_username']:
                    search_result = search_result.filter(
                        author__username=request.POST['author_username'])
                if request.POST['date_field']:
                    search_result = search_result.filter(
                        created_at__gt=request.POST['date_field'])
    else:
        form = SearchForm()

    return render(request, 'search.html', locals())
