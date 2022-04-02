from turtle import pos, title
from unicodedata import category
from urllib import response
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from pip import main
from .models import Post, Category, User

# Create your tests here.

class TestView(TestCase) :
    def setUp(self) :
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump',password='someword')
        self.user_obama = User.objects.create_user(username='obama',password='someword')
        self.user_trump.is_staff = True
        self.user_trump.save()

        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')

        self.post_001 = Post.objects.create(
            title='첫번째 포스트입니다.',
            content='Hello World. We are the world.',
            category=self.category_programming,
            author=self.user_trump,
        )
        

    def test_post_list(self) :
        response = self.client.get('/portfolio/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Portfolio')
        navbar = soup.nav
        self.assertIn('Home', navbar.text)
        self.assertIn('About', navbar.text)
        # self.assertEqual(Post.objects.count(), 0)
        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)
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
        # self.assertEqual(Post.objects.count(), 2)
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
        self.assertEqual(post_001.get_absolute_url(), '/portfolio/2/')
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

        self.client.login(username='obama', password='someword')
        response = self.client.get('/portfolio/create_post/')
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='trump', password='someword')
        response = self.client.get('/portfolio/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual('Create Post - Portfolio', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)

        self.client.post(
            '/portfolio/create_post/',
            {
                'title' : 'Post Form 만들기',
                'content' : 'Post Form 페이지 만들기 중',
            }
        )

        last_post = Post.objects.last()
        self.assertEqual(last_post.title, "Post Form 만들기")
        self.assertEqual(last_post.author.username, "trump")


    def test_update_post(self) :
        update_post_url = f'/portfolio/update_post/{self.post_001.pk}/'

        # 로그인 하지 않은 경우
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)

        # 로그인은 했지만 작성자가 아닌 경우
        self.assertNotEqual(self.post_001.author, self.user_obama)
        self.client.login(
            username = self.user_obama.username,
            password = 'someword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)

        # 작성자가 접근하는 경우
        self.client.login(
            username = self.post_001.author.username,
            password = 'someword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Post - Portfolio', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)

        # tag_str_input = main_area.find('input', id='id_tags_str')
        # self.assertTrue(tag_str_input)
        # self.assertIn('파이썬 공부; python', tag_str_input.attrs['value'])

        response = self.client.post(
            update_post_url,
            {
                'title' : '첫번째 포스트를 수정했습니다.' ,
                'content' : '나에게 천재일우의 기회가 왔다' ,
                'category' : self.category_music.pk ,
                # 'tags_str' : '파이썬 공부; 한글태그, some tag'
            },
            follow=True
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        post_area = soup.find('section', id='post-area')
        self.assertIn('첫번째 포스트를 수정했습니다.', main_area.text)
        self.assertIn('나에게 천재일우의 기회가 왔다', post_area.text)
        self.assertIn(self.category_music.name, main_area.text)
        # self.assertIn('파이썬 공부', main_area.text)
        # self.assertIn('한글태그', main_area.text)
        # self.assertIn('some tag', main_area.text)
        # self.assertNotIn('python', main_area.text)


    def test_delete_post(self) :
        post_by_trump = Post.objects.create(
            post = self.post_001,
            author = self.user_trump,
            content = '트럼프의 글입니다.'
        )
        
        self.assertEqual(Post.objects.count(), 1)

        self.client.login(username='trump', password='someword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div', id='main-area')
        self.assertFalse(main_area.find('a', id='post-delete-button'))
        post_delete_btn = main_area.find('a', id='post-delete-button')
        self.assertIn('Delete', post_delete_btn.text)
        
        delete_post_modal = soup.find('div', id='DeletePostModal')
        self.assertIn('Are you Sure?', delete_post_modal.text)
        really_delete_btn = delete_post_modal.find('a')
        self.assertIn('Delete', really_delete_btn.text)
        self.assertIn(
            really_delete_btn.attrs['href'],
            '/portfolio/delete_post/1/'
        )

        response = self.client.get('/portfolio/delete_post/1/', follow=True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(Post.objects.count(), 0)








