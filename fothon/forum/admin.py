from django.contrib import admin
from forum.models import ForumUser
from forum.models import Category
from forum.models import Topic
from forum.models import Post

# Register your models here.
admin.site.register(ForumUser)
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Post)