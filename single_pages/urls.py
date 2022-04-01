from django.urls import path
from . import views
# from blog.views import LatestView

urlpatterns = [
    path('about_me/', views.about_me),
    path('', views.landing),
    # path('', LatestView.as_view()),
]