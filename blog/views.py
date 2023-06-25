from blog.models import Post
from kollektiivi.signals import site_tracker
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView


class HomeView(ListView):

    template_name = 'blog/home.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        site_tracker.send(sender=None, request=request)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):

        result_list = Post.objects.filter(active=True).order_by('-display_date')
        return result_list


class PostView(TemplateView):

    template_name = 'blog/post-full.html'

    def get(self, request, *args, **kwargs):
        site_tracker.send(sender=None, request=request)
        preview = request.GET.get("preview", 0)
        if preview == "1":
            self.object = get_object_or_404(Post, slug=kwargs['post_slug'])
        else:
            self.object = get_object_or_404(Post, slug=kwargs['post_slug'], active=True)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = self.object
        return context
