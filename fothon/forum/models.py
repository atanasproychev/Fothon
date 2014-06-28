from django.db import models
from django.contrib.auth.models import User


TYPES = (
    ('R', 'Regular'),
    ('S', 'Special'),
)


class ForumUser(User):
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = models.CharField(max_length=1, choices=GENDERS,
                              null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.get_full_name()


class Category(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField()
    parent = models.ForeignKey('self', null=True, blank=True)
    type = models.CharField(max_length=1, choices=TYPES, default='R')

    def __str__(self):
        return "{0}.{1}".format(self.order, self.title)


class Topic(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('ForumUser')
    category = models.ForeignKey('Category')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_from = models.ForeignKey('ForumUser',
                                           related_name="last_modified_from")

    def posts(self):
        return len(self.post_set.values())

    def __str__(self):
        return "{0} > {1}".format(self.category, self.title)


class Post(models.Model):
    text = models.CharField(max_length=500)
    author = models.ForeignKey('ForumUser')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey('Topic')

    def __str__(self):
        return "{0} > {1}".format(self.topic, self.text)
