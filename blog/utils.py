from blog.models import Blog

def get_posts(no_records=5):
    return Blog.objects.filter(active=True)[:no_records]