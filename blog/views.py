from blog.models import Blog
from kollektiivi.signals import site_tracker
from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic import TemplateView


class HomeView(TemplateView):
    def get(self, request):
        site_tracker.send(sender=None, request=request)
        news = Blog.objects.filter(active=True).order_by('-display_date')
        paginator = Paginator(news, 5)

        try:
            page = int(request.GET. get('page', '1'))
        except ValueError:
            page = 1

        try:
            news = paginator.page(page)
        except (EmptyPage, InvalidPage):
            news = paginator.page(paginator.num_pages)

        return render(request,
                      'blog/home.html',
                      {'page': news,
                       'news_active': True})


class BlogView(TemplateView):
    def get(self, request, blog_slug):
        site_tracker.send(sender=None, request=request)
        preview = request.GET.get("preview", 0)
        if preview == "1":
            blog = Blog.objects.get(slug=blog_slug)
        else:
            blog = Blog.objects.get(slug=blog_slug, active=True)
        return render(request,
                      'blog/blog-full-post.html',
                      {'blog': blog,
                       'news_active': True})
