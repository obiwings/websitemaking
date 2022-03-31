from re import template
from django.shortcuts import render
from .models import Post, Category
from django.views.generic import ListView, DetailView

# Create your views here.

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