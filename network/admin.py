from django.contrib import admin
from .models import Follow, Post, User, Like, UserInformation

# Register your models here.

# admin.site.register(Post, PostAdmin)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Post)
admin.site.register(User)
admin.site.register(UserInformation)