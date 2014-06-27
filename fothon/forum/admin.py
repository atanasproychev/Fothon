from django.contrib import admin
from django.contrib.auth.models import User
from forum.models import ForumUser
from forum.models import Category
from forum.models import Topic
from forum.models import Post

# Register your models here.
admin.site.unregister(User)

class ForumUserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information', {'fields': ['username', 'password', 'email']}),
        ('Profile information', {'fields': ['first_name', 'last_name', 'picture', 'gender', 'city', 'birth_date']}),
        ('User information', {'fields': ['is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions', 'date_joined', 'last_login']}),
    ]# add other fields
admin.site.register(ForumUser, ForumUserAdmin)
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Post)