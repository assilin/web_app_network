import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse


from .models import Follow, Like, Post, User, UserInformation

# adding to the post information about likes/dislikes
def add_like_info(posts, current_user):
    for post in posts:
        post.likes = post.like_post.filter(like_dislike="Li")
        check_like = False
        for item in post.likes:
            if item.like_user == current_user:
                check_like = True
        post.check_like = check_like

        post.dislikes = post.like_post.filter(like_dislike="Di")
        check_dislike = False
        for item in post.dislikes:
            if item.like_user == current_user:
                check_dislike = True
        post.check_dislike = check_dislike
    return


def index(request):
    # post paginator
    all_posts = Post.objects.all().order_by("-date")
    # paginator = Paginator(all_posts, 2)
    paginator = Paginator(all_posts, 10)
    current_page = request.GET.get('page')
    page_posts = paginator.get_page(current_page)

    current_user = request.user

    add_like_info(page_posts, current_user)

    return render(request, "network/index.html", {
        "pagePosts": page_posts,
    })


# new post
@login_required
def new_post(request):
    if request.method == "POST":
        new_post = Post(
            text = request.POST["postContent"],
            author = request.user,
        )
        new_post.save()
        return HttpResponseRedirect(reverse("index"))


# edit post
@login_required
def edit_post(request, post_id):
    if request.method == "PUT":
        post_to_edit = Post.objects.get(id=post_id)

        data = json.loads(request.body)
        # if data.get("text") is not None:
        post_to_edit.text = data["text"]
        post_to_edit.save()

        return JsonResponse({
            "message": "post has been edited",
            "data": data["text"]
        })


# like/dislike function
def like_dislike(request, post_id):
    if request.method == "PUT":
        current_user = request.user
        try:
            like_object = Like.objects.filter(like_user=current_user).get(like_post=Post.objects.get(pk=post_id))
        except ObjectDoesNotExist:
            like_object = Like(
                like_user = current_user,
                like_post = Post.objects.get(pk=post_id),
                like_dislike = "No"
            )
            like_object.save()
        data = json.loads(request.body)

        if data["like_or_dislike"] == "like":
            check_like = (data["like_dislike_status"] == "true" or data["like_dislike_status"] == True)
            # print(like_status)
            # print(data["check_like"])
            # print(check_like)
            # print(not check_like)
            if check_like:
                like_object.like_dislike = "No"
                # new_like_status = True
            else:
                like_object.like_dislike = "Li"
                # new_like_status = False
            like_object.save()
            # print(Like.objects.filter(like_user=current_user).get(like_post=Post.objects.get(id=post_id)))

            return JsonResponse({
                "message": "like status changed",
                "newLikeStatus": not check_like
            })
        else:
            check_dislike = (data["like_dislike_status"] == "true" or data["like_dislike_status"] == True)
            if check_dislike:
                like_object.like_dislike = "No"
            else:
                like_object.like_dislike = "Di"
            like_object.save()

            return JsonResponse({
                "message": "like status changed",
                "newDislikeStatus": not check_dislike
            })


# profile
@login_required
def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    try:
        user_info = UserInformation.objects.get(userinfo_id=profile_user)
    except ObjectDoesNotExist:
        user_info = UserInformation(userinfo_id=profile_user)
    current_user = request.user

    following = Follow.objects.filter(user_f_ing=profile_user)
    followers = Follow.objects.filter(user_f_ed=profile_user)

    all_posts = Post.objects.filter(author=profile_user).order_by("-date")
    # paginator = Paginator(all_posts, 2)
    paginator = Paginator(all_posts, 10)
    current_page = request.GET.get('page')
    page_posts = paginator.get_page(current_page)

    try:
        check_follow = followers.filter(user_f_ing=User.objects.get(pk=current_user.id))
        is_follow = True if len(check_follow) > 0 else False
    except ObjectDoesNotExist:
        is_follow = False

    add_like_info(page_posts, current_user)

    return render(request, "network/profile.html", {
        "pagePosts": page_posts,
        "profileUser": profile_user,
        "userInfo": user_info,
        "following": following,
        "followers": followers,
        "isFollow": is_follow,
    })


@login_required
def edit_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    try:
        user_info = UserInformation.objects.get(userinfo_id=user)
    except ObjectDoesNotExist:
        user_info = UserInformation(userinfo_id=user)

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        first_name = request.POST["firstName"]
        last_name = request.POST["lastName"]

        if password != confirmation:
            return render(request, "network/editProfile.html", {
                "message": "Passwords must match.",
                "user": user
            })

        # date_of_birth = request.POST["dateOfBirth"]
        about = request.POST["about"]
        url_img = request.POST["imageURL"]
        date_of_birth = None if request.POST["dateOfBirth"] == "" else request.POST["dateOfBirth"]

        user_info.date_of_birth = date_of_birth
        user_info.about = about
        user_info.img = url_img
        user_info.save()

        if username != user.username and User.objects.filter(username=username).exists():
            return render(request, "network/editProfile.html", {
                "message": "Username already exists.",
                "user": user
            })
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        if password != "":
            user.set_password(password)
        user.save()

        logout(request)
        login(request, user)


        return HttpResponseRedirect(reverse("index"))

    return render(request, "network/editProfile.html", {
        "userInfo": user_info
    })


def follow(request):
    if request.method == "POST":
        user_to_follow = User.objects.get(username=request.POST["followUser"])
        current_user = request.user
        new_connection = Follow(
            user_f_ing=current_user,
            user_f_ed=user_to_follow,
        )
        new_connection.save()
        return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_to_follow.id}))


def unfollow(request):
    if request.method == "POST":
        user_to_unfollow = User.objects.get(username=request.POST["unfollowUser"])
        current_user = request.user
        del_connection = Follow.objects.get(
            user_f_ing=current_user,
            user_f_ed=user_to_unfollow,
        )
        del_connection.delete()
        return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_to_unfollow.id}))

@login_required
def following(request):
    all_following = Follow.objects.filter(user_f_ing=request.user).values_list('user_f_ed', flat=True)
    all_posts = Post.objects.filter(author__in=all_following).order_by("-date")
    # paginator = Paginator(all_posts, 2)
    paginator = Paginator(all_posts, 10)
    current_page = request.GET.get('page')
    page_posts = paginator.get_page(current_page)

    current_user = request.user
    add_like_info(page_posts, current_user)

    return render(request, "network/following.html", {
        "pagePosts": page_posts
    })


# login / logout / register functions
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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        # ADD USER'S INFO
        user_info = UserInformation(userinfo_id=user)
        return render(request, "network/editProfile.html", {
            "userInfo": user_info
        })

    else:
        return render(request, "network/register.html")
