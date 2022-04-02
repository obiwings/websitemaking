from django.urls import path
from . import views
from blog.views import LatestList


urlpatterns = [
    path('about_me/', views.about_me),
    path('', views.landing),
    path('', LatestList.as_view()),
]