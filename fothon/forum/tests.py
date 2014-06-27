from django.test import TestCase

from django.contrib.auth.models import Group

from forum.models import Category
from forum.models import Topic
from forum.models import Post
from forum.models import ForumUser

# Create your tests here.
class ForumViewsTestCase(TestCase):
    def setUp(self):
        main = Category.objects.create(title='Main', order=0)
        Category.objects.create(title='First', order=1, parent=main)
        category = Category.objects.create(title='Second', order=2, parent=main)
        Category.objects.create(title='ThirdSpecial', order=3, parent=main, type='S')
        subcategory = Category.objects.create(title='SubCategory', order=1, parent=category)
        Category.objects.create(title='SubCategorySpecial', order=2, parent=category, type='S')
        user = ForumUser.objects.create_user(username='specialuser', password='222222')
        group = Group.objects.create(name='SpecialUser')
        user.groups = [group]
        Topic.objects.create(title='Topic', author=user, category=subcategory, last_modified_from=user)
    
    def test_index(self):
        response = self.client.get("/fothon/")
        self.assertEqual(response.status_code, 200)
        
    def test_index_with_special_user(self):
        self.client.login(username='specialuser', password='222222')
        response = self.client.get("/fothon/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_special'])
        
    def test_category_view(self):
        response = self.client.get("/fothon/5/")
        self.assertEqual(response.status_code, 200)
        
    def test_topic_view(self):
        response = self.client.get("/fothon/topic/1/")
        self.assertEqual(response.status_code, 200)
        
    def test_new_content_view_unregistered_user(self):
        response = self.client.get("/fothon/topic/1/new/")
        self.assertEqual(response.status_code, 302)
        
    def test_new_content_view_registered_user(self):
        self.client.login(username='specialuser', password='222222')
        response = self.client.get("/fothon/topic/1/new/")
        self.assertEqual(response.status_code, 200)
        
    def test_new_content_view_create_post(self):
        self.client.login(username='specialuser', password='222222')
        num_posts = Topic.objects.get(pk=1).post_set.count()
        response = self.client.post("/fothon/post/1/new/?back=/fothon/", {'content': "New post"})
        new_num_posts = Topic.objects.get(pk=1).post_set.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_num_posts, num_posts + 1)
        
    def test_new_content_view_create_topic(self):
        self.client.login(username='specialuser', password='222222')
        num_topics = Category.objects.get(pk=2).topic_set.count()
        response = self.client.post("/fothon/topic/2/new/?back=/fothon/", {'content': "New topic"})
        new_num_topics = Category.objects.get(pk=2).topic_set.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_num_topics, num_topics + 1)
        
    def test_login_invalid_username(self):
        response = self.client.post("/fothon/login/", {'username': "username", 'password': "password"})
        self.assertEqual(response.status_code, 200)
        
    def test_login(self):
        response = self.client.post("/fothon/login/", {'username': "specialuser", 'password': "222222"})
        self.assertEqual(response.status_code, 302)
        
    def test_register(self):
        response = self.client.post("/fothon/register/", {'username': "username", 'password': "password", 'email': "email@example.com"})
        self.assertEqual(response.status_code, 302)
        
    def test_register_already_existing_user(self):
        response = self.client.post("/fothon/register/", {'username': "specialuser", 'password': "password", 'email': "email@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already exists")
