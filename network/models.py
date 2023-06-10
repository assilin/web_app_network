from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class UserInformation(models.Model):
    # userinfo_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name="name")
    userinfo_id = models.OneToOneField(User, on_delete=models.PROTECT)
    img = models.CharField(max_length=1000, blank=True)
    about = models.CharField(max_length=1000, blank=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)


class Post(models.Model):
    text = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="author_name")
    date = models.DateTimeField(default=timezone.now)
    number_of_likes = models.IntegerField(blank=True, null=True)
    number_of_dislikes = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"PostID {self.id} posted by {self.author} on {self.date}"


class Follow(models.Model):
    user_f_ing = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    user_f_ed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed")

    # unique following
    class Meta:
        unique_together = ("user_f_ing", "user_f_ed")

    def clean(self):
        if self.user_f_ing == self.user_f_ed:
            raise ValidationError('user_f_ing and user_f_ed must be different')

    def __str__(self):
        return f"{self.user_f_ing} follow {self.user_f_ed}"

class Like(models.Model):
    like_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="like_user")
    like_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like_post")
    like = "Li"
    dislike = "Di"
    nolike = "No"

    like_dislike_choice = [
        (like, "Like"),
        (dislike, "Dislike"),
        (nolike, "Nolike"),
    ]
    like_dislike = models.CharField(
        max_length=2,
        choices=like_dislike_choice,
        default=nolike,
    )

    # unique likes
    class Meta:
        unique_together = ("like_user", "like_post")

    def __str__(self):
        return f"{self.like_user} set {self.like_dislike} to post {self.like_post}"
