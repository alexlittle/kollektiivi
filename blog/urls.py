from django.urls import path

from blog import views as blog_views
from blog.feeds import LatestNews

app_name = 'blog'

urlpatterns = [
    path('', blog_views.HomeView.as_view(), name="uutiset"),
    path('feed/', LatestNews(), name="feed"),
    path('<post_slug>', blog_views.PostView.as_view(), name="post")
]
