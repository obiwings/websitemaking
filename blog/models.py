from pyexpat import model
from tabnanny import verbose
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os

# Create your models here.

class Tag(models.Model) :
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self) :
        return self.name

    def get_absolute_url(self) :
        return f'/portfolio/tag/{self.slug}/'



class Category(models.Model) :
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    def __str__(self) :
        return self.name

    def get_absolute_url(self) :
        return f'/portfolio/category/{self.slug}/'

    class Meta :
        verbose_name_plural = 'Categories'

        

class Post(models.Model) :
    title = models.CharField(max_length=45)
    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self) :
        return f'{self.pk}. {(self.title)} :: {self.author}'

    def get_absolute_url(self) :
        return f'/portfolio/{self.pk}/'

    def get_content_markdown(self) :
        return markdown(self.content)