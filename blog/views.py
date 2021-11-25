from datetime import timedelta
import datetime
from django.http import response
from django.shortcuts import redirect, render
from django.utils import timezone
from .models import Post, User, Session
from django.shortcuts import render, get_object_or_404
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def login(request):
    error = ""
    if request.method == "POST":
        login = request.POST.get("login")
        password = request.POST.get("password")
        url = request.POST.get("continue", "/")
        sessid = do_login(login, password)
        if sessid:
            response = HttpResponseRedirect(url)
            response.set_cookie("sessid", sessid,
                domain="site.com", httponly=True,
                expires = datetime.now() + timedelta(days=30)
            )
            return response
        else:
            error = u"Неверный логин / пароль"
    return render(request, "login.html", {"error": error})


def do_login(login, password):
    try:
        user = User.objects.get(login=login)
    except User.DoesNotExist:
        return None
    hashed_pass = salt_and_hash(password)
    if user.password != hashed_pass:
        return None
    session = Session()
    session.key = generate_long_random_key()
    session.user = user
    session.expires = datetime.now() + timedelta(days=30)
    session.save()
    return session.key


def logout(request):
    sessid = request.COOKIE.get("sessid")
    if sessid is not None:
        Session.objects.delete(key=sessid)
    url = request.GET.get("continue", "/")
    return HttpResponseRedirect(url)


