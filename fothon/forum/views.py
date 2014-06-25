from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from forum.forms import LoginForm
from forum.forms import RegisterForm
from forum.forms import ProfileForm
from forum.forms import NewContentForm
from forum.models import ForumUser
from forum.models import Category
from forum.models import Topic
from forum.models import Post


def index(request):
    print(dir(request))
    #print(dir(request.user))
    main_category = Category.objects.get(title='Main')
    
    return render(request, 'index.html', locals())
    
def category_view(request, category_id):
    topics = Topic.objects.filter(category_id=category_id).order_by('-last_modified')
    
    return render(request, 'category.html', locals())
    
def topic_view(request, topic_id):
    posts = Post.objects.filter(topic_id=topic_id).order_by('created_at')
    
    return render(request, 'topic.html', locals())
    
def new_content_view(request, content_type, content_id):
    if content_type not in ('topic', 'post'):
        return redirect('/fothon')
    print(content_type)
    print(content_id)
    if request.method == 'POST':
        form = NewContentForm(request.POST)
        if form.is_valid():
            content = request.POST['content']
            user = ForumUser.objects.get(username=request.user.username)
            if content_type == 'topic':
                attr = 'title'
                parent = 'category_id'
                Topic.objects.create(title=content, category_id=content_id, author=user, last_modified_from=user)
            elif content_type == 'post':
                attr = 'text'
                parent = 'topic_id'
                Post.objects.create(text=content, topic_id=content_id, author=user)
            print(dir(request))
            print(request.REQUEST)
            return redirect(request.REQUEST.back)
    else:
        print(request.REQUEST)
        form = NewContentForm()
    
    return render(request, 'new_content.html', locals())
    
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            print(request.POST)
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
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            #user = ForumUser.objects.get(username=username)
            user = None
            print(user2)
            if user is None:
                ForumUser.objects.create_user(username, email, password)
                return redirect('/fothon')
            else:
                return HttpResponse("You are not registered!")
    else:
        form = RegisterForm()
        
    return render(request, 'register.html', locals())
    
def logout_view(request):
    logout(request)
    return redirect('/fothon')

def profile_view(request):
    print(request.user.username)
    u = ForumUser.objects.get(username=request.user.username)
    d=dict(u)
    print(d)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            #user = ForumUser.objects.get(username=username)
            user = None
            print(user2)
            if user is None:
                ForumUser.objects.create_user(username, email, password)
                return redirect('/fothon')
            else:
                return HttpResponse("You are not registered!")
    else:
        form = ProfileForm(u)
        
    print(form.as_p())
        
    return render(request, 'profile.html', locals())
    
