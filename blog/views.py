from re import template
from django.shortcuts import render
from .models import Post
from django.views.generic import ListView

# Create your views here.

class PostList(ListView) :
    model = Post
    ordering = '-pk'
    template_name = 'page/portfolio.html'


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