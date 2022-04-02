from dataclasses import field
from gc import get_objects
import imp
from inspect import CORO_RUNNING
from pyexpat.errors import messages
from re import U, template
import re
from turtle import pos
from urllib import response
from wsgiref.util import request_uri
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CreatePost
# from .forms import PostForm

# Create your views here.

# class LatestView(ListView) :
#     model = Post
#     ordering = '-pk'
#     template_name = 'page/home.html'

#     def get_context_data(self, **kwargs) :
#         context = super(PostList, self).get_context_data()
#         context['categories'] = Category.objects.all()
#         context['no_category_post_count'] = Post.objects.filter(category=None).count()
#         return context


class LatestList(ListView) :
    model = Post
    ordering = '-pk'
    template_name = 'page/home.html'

    def get_context_data(self, **kwargs) :
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context




    
class PostList(ListView) :
    model = Post
    ordering = '-pk'
    template_name = 'page/portfolio.html'

    def get_context_data(self, **kwargs) :
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView) :
    model = Post
    template_name = 'page/portfolio_detail.html'


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView) :
    model = Post
    template_name = 'page/post_form.html'
    # fields = [ 'title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', ]
    form_class = CreatePost

    def test_func(self) :
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form) :
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str :
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',',';')
                tags_list = tags_str.split(';')

                for t in tags_list :
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created :
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else :
            return redirect('/portfolio/')


class PostUpdate(LoginRequiredMixin, UpdateView) :
    model = Post
    template_name = 'page/post_update_form.html'
    # fields = [ 'title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', ]
    form_class = CreatePost


    def get_context_data(self, **kwargs) :
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists() :
            tags_str_list = list()
            for t in self.object.tags.all() :
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)
        return context

    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated and request.user == self.get_object().author :
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else :
            raise PermissionDenied

    def form_valid(self, form) :
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str :
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',',';')
            tags_list = tags_str.split(';')

            for t in tags_list :
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created :
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response


def portfolio_delete(request, pk) :
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author :
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('/portfolio/')
    post.delete()
    return redirect('/portfolio/')




# def delete_post(request, pk) :
#     post = Post.objects.get(pk=pk)
#     if request.user.is_authenticated and request.user == post.author :
#         post.delete()
#         return redirect('/portfolio/')
#     else :
#         raise PermissionDenied





# def DeletePost(request, pk):
#     post = Post.objects.get(pk=pk)
#     # post.
#     return redirect('/portfolio/')



# def del_qna(request, pk) :
#     if request.session.get('userid'):
#         del_portfolio = Post.objects.get(pk=pk)
#         del_portfolio.delete()
#         return redirect('../portfolio')
#     else :
#         return redirect('../portfolio')



# def portfolio(request) :
#     posts = Post.objects.all()

#     return render(
#         request,
#         'page/portfolio.html',
#         {
#             'posts' : posts,
#         }
#     )

def portfolio_details(request, pk) :
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'page/portfolio_detail.html',
        {
            'post' : post,
        }
    )

def category_page(request, slug) :
    
    if slug == 'no_category' :
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'page/portfolio.html',
        {
            'post_list' : post_list,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
            'category' : category,
        }
    )


# def home(request) :
#     return render(request, 'page/home.html')

# def post_create(request) :
#     if request.method == "POST" :
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save()
#             return redirect('home')
        
#         else :
#             form = PostForm()

#         context = {
#             'form' : form
#         }
#         return render(request, 'page/post_form.html')