from django.db import models
from django.contrib.auth.models import User


class ForumUser(User):
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    picture = models.ImageField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS, null=True)
    city = models.CharField(max_length=50, null=True)
    birth_date = models.DateField(null=True)
    categories = models.ManyToManyField('Category')
    
    def __str__(self):
        return self.get_full_name()
    
class Category(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField()
    parent = models.ForeignKey('self')
    
    def __str__(self):
        return "%d.%s".format(self.order, self.title)
        
class Topic(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('ForumUser')
    category = models.ForeignKey('Category')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_from = models.ForeignKey('ForumUser', related_name="last_modified_from")
    
    def __str__(self):
        return "%s > %s".format(self.category, self.title)
        
class Post(models.Model):
    text = models.CharField(max_length=500)
    author = models.ForeignKey('ForumUser')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey('Topic')
    
    def __str__(self):
        return "%s > %s".format(self.topic, self.text)