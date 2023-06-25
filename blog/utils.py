from blog.models import Post


def get_posts(no_records=5):
    return Post.objects.filter(active=True)[:no_records]
