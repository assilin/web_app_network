
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("editProfile/<int:user_id>", views.edit_profile, name="editProfile"),
    path("following", views.following, name="following"),
    path("followUser", views.follow, name="followUser"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("register", views.register, name="register"),
    path("newPost", views.new_post, name="newPost"),
    path("unfollowUser", views.unfollow, name="unfollowUser"),

    # API Routes
    path("editPost/<int:post_id>", views.edit_post, name="editPost"),
    path("likeOrDislike/<int:post_id>", views.like_dislike, name="like_dislike"),
]
