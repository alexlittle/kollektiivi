from django.urls import path

from blog import views as blog_views
from blog.feeds import LatestNews

app_name = 'blog'

urlpatterns = [
    path('', blog_views.HomeView.as_view(), name="home"),
    path('feed/', LatestNews(), name="feed"),
    path('<blog_slug>', blog_views.BlogView.as_view(), name="article")
]
