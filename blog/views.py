from re import template
from .models import Post
from django.views.generic import ListView, DetailView

# Create your views here.

class PostList(ListView) :
    model = Post
    ordering = '-pk'
    template_name = 'page/portfolio.html'

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