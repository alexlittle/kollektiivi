from django.contrib.syndication.views import Feed
from django.urls import reverse
from blog.models import Post


class LatestNews(Feed):
    description_template = 'blog/feed.html'
    title = "Kollektiivi - Uutiset"
    link = "/uutiset/"
    description = ""

    def items(self):
        return Post.objects.filter(active=True).order_by('-display_date')[:20]

    def item_title(self, item):
        return item.title

    def item_body(self, item):
        return item.body

    def item_link(self, item):
        return reverse('blog:post', args={item.slug})
