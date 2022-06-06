from django.contrib.auth.models import User
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Profile, Post
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
# Create your views here.


def Home(request):
    if not request.user.is_authenticated:
        return('Login')
    profile_id = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user=request.user)
    return render(request, 'base/home.html', {"posts": posts})


def Login(request):
    if request.user.is_authenticated:
        return redirect("profile")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("profile")
    return render(request, 'base/Login.html')


def Logout(request):
    logout(request)
    return redirect("Login")


def signup(request):
    if request.user.is_authenticated:
        return redirect("profile")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        image = request.FILES['image']
        bio = request.POST['bio']
        user = User.objects.create_user(username=username, password=password)
        profile = Profile.objects.create(
            user=user, profile_picture=image, discrip=bio)
        if profile:
            messages.success(request, 'Profile Created Please Login')
            return redirect("Login")
    return render(request, 'base/Signup.html')


def profile(request, id=None):
    if not request.user.is_authenticated:
        return redirect("Login")
    if id is not None:
        profile_id = Profile.objects.get(id=id)
        posts = Post.objects.filter(profile=profile_id)
        posts_num = posts.count()
        profile = Profile.objects.get(user=request.user)
        profile_image = profile.profile_picture.url
    else:
        profile_id = Profile.objects.get(user=request.user)
        posts = Post.objects.filter(user=request.user)
        posts_num = posts.count()
        profile_image = profile_id.profile_picture.url
    return render(request, 'base/profile.html', {'profile': profile_id, 'profileimage': profile_image, 'profile_of_user': True, 'posts': posts, 'posts_num': posts_num})


def add_post(request):
    if not request.user.is_authenticated:
        return redirect("Login")
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url
    if request.method == 'POST':
        post = request.FILES['image']
        profile = Profile.objects.get(user=request.user)
        posts = Post.objects.create(
            user=request.user, image=post, profile=profile)
        if posts:
            messages.success(request, "POST Uploaded")
    return render(request, 'base/addposts.html', {'profileimage': profileimage})


def like(request, id):
    post = Post.objects.filter(id=id)
    if request.user in post[0].likes.all():
        post[0].likes.remove(request.user)
    else:
        post[0].likes.add(request.user)
    return redirect("home")


def search(request):
    if not request.user.is_authenticated:
        return redirect("Login")
    profile = Profile.objects.get(user=request.user)
    profileimage = profile.profile_picture.url
    search = request.GET['username']
    profiles = Profile.objects.filter(user__username__icontains=search)
    context = {'profiles': profiles, 'username': search,
               "profileimage": profileimage}
    return render(request, 'base/search.html', context)


def follow(request, id, username):
    profile = Profile.objects.get(id=id)
    Login_profile = Profile.objects.get(user=request.user)
    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
        Login_profile.followings.remove(profile.user)
    else:
        profile.followers.add(request.user)
        Login_profile.followings.add(profile.user)
    return redirect(f'/search?username={username}')
