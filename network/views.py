from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json


from .models import *


def index(request):
    posts_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts_list, 10)
    if 'page' in request.GET:
        page_number = request.GET['page']
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    
    pages = []
    for i in range(1, page_obj.paginator.num_pages+1):
        pages.append(i)

    return render(request, "network/index.html", {
        "heading" : "All Posts",
        "posts" : page_obj,
        "range" : pages,
        "new_post" : True
    })

@login_required
def following(request):
    posts = Post.objects.none()
    user = User.objects.get(username=request.user)
    follow = Follow.objects.get(person=user)
    followed_users = follow.following.all()
    for followed_user in followed_users:
        post = followed_user.posts.all()
        posts |= post
    posts_list =  posts.order_by('-timestamp')
    paginator = Paginator(posts_list, 10)
    if 'page' in request.GET:
        page_number = request.GET['page']
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    pages = []
    for i in range(1, page_obj.paginator.num_pages+1):
        pages.append(i)
    return render(request, "network/index.html", {
        "heading" : "Following",
        "posts" : page_obj,
        "range" : pages,
        "new_post" : False
    })

@login_required
def new_post(request, username):
    if request.method == 'POST':
        poster = User.objects.get(username=username)
        post = Post()
        post.posted_by = poster
        post.body = request.POST['content']
        post.save()
    return redirect('index')

@csrf_exempt
@login_required
def like(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        user = User.objects.get(username=request.user)
        post.likes.add(user)
        return JsonResponse({"message": "Post liked successfully."}, status=201)
    return JsonResponse({"error": "POST request required."}, status=400)

@csrf_exempt
@login_required
def unlike(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        user = User.objects.get(username=request.user)
        post.likes.remove(user)
        return JsonResponse({"message": "Post unliked successfully."}, status=201)
    return JsonResponse({"error": "POST request required."}, status=400)

@csrf_exempt
@login_required
def edit(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        data = json.loads(request.body)
        post.body = data.get("body", "")
        post.save()
        return JsonResponse({"message": "Post edited successfully."}, status=201)
    return JsonResponse({"error": "POST request required."}, status=400)

def profile(request, username):
    user = User.objects.get(username=username)
    posts_list = user.posts.all().order_by('-timestamp')
    paginator = Paginator(posts_list, 10)
    if 'page' in request.GET:
        page_number = request.GET['page']
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    pages = []
    for i in range(1, page_obj.paginator.num_pages+1):
        pages.append(i)
    follow = Follow.objects.get(person=user)
    if request.user.is_authenticated:
        main = Follow.objects.get(person=request.user)
        if main.following.filter(username=username):
            unfollow_button = 'inline-block'
            follow_button = 'none'
        else:
            follow_button = 'inline-block'
            unfollow_button = 'none'
    else:
        follow_button = None
        unfollow_button = None
    return render(request, "network/profile.html", {
        "username" : username,
        "image" : username[0],
        "followers" : follow.followers,
        "following" : follow.following.count(),
        "follow" : follow_button,
        "unfollow" : unfollow_button, 
        "posts" : page_obj,
        "range" : pages
    })

@csrf_exempt
def follow(request, username):
    followed = username
    followed = User.objects.get(username=followed)
    if request.method == "POST":
        main_user = Follow.objects.get(person=request.user)
        other_user = Follow.objects.get(person=followed)
        other_user.followers += 1
        other_user.save()
        main_user.following.add(followed)
        return JsonResponse({"message": "Followed successfully."}, status=201)
    return JsonResponse({"error": "POST request required."}, status=400)

@csrf_exempt
def unfollow(request, username):
    unfollowed = username
    unfollowed = User.objects.get(username=unfollowed)
    if request.method == "POST":
        main_user = Follow.objects.get(person=request.user)
        other_user = Follow.objects.get(person=unfollowed)
        other_user.followers -= 1
        other_user.save()
        main_user.following.remove(unfollowed)
        return JsonResponse({"message": "Unfollowed successfully."}, status=201)
    return JsonResponse({"error": "POST request required."}, status=400)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            follow = Follow()
            follow.person = user
            follow.followers = 0
            follow.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
