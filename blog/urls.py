from django.urls import path
from . import views



urlpatterns = [
    path('about_me/', views.about_me),
    path('', views.landing),
    path('<int:pk>/delete/', views.portfolio_delete, name='portfolio_delete'),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('portfolio/', views.PostList.as_view()),
    path('portfolio/', views.portfolio)
    # path('create_post/', views.post_create, name='home'),
    # path('<int:pk>/', views.portfolio_details),
    # path('', views.portfolio),
]
