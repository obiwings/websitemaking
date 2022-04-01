from turtle import pos, title
from unicodedata import category
from urllib import response
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category, User

# Create your tests here.

class TestView(TestCase) :
    def setUp(self) :
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump',password='someword')
        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')
        

    def test_post_list(self) :
        response = self.client.get('/portfolio/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Portfolio')
        navbar = soup.nav
        self.assertIn('Home', navbar.text)
        self.assertIn('About', navbar.text)
        self.assertEqual(Post.objects.count(), 0)
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)
        post_001 = Post.objects.create(
            title = '첫 번째 포스트',
            content = '첫 포스트 입니다.',
            category = self.category_programming,
            author = self.user_trump,
        )
        post_002 = Post.objects.create(
            title = '두 번째 포스트',
            content = '2 포스트 입니다.',
            category = self.category_music,
        )
        self.assertEqual(Post.objects.count(), 2)
        response = self.client.get('/portfolio/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

    def test_post_detail(self) :
        post_001 = Post.objects.create(
            title = '첫 번째 포스트',
            content = 'Hello world. We are the world.',
        )
        self.assertEqual(post_001.get_absolute_url(), '/portfolio/1/')
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        navbar = soup.nav
        self.assertIn('Home', navbar.text)
        self.assertIn('About', navbar.text)
        self.assertIn(post_001.title, soup.title.text)
        main_area = soup.find('div', id='main-area')
        post_area = soup.find('section', id='post-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_001.content, post_area.text)

    def test_create_post(self) :
        response = self.client.get('/portfolio/create_post/')
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='trump', password='someword')

        response = self.client.get('/portfolio/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Create Post - Portfolio', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)


