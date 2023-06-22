from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from kollektiivi.models import Page, Tag


class HomeView(TemplateView):

    template_name = 'kollektiivi/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(slug='home')
        return context


class PageView(TemplateView):

    template_name = 'kollektiivi/page.html'

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Page, slug=kwargs['slug'], active=True)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.object
        return context


class TagView(TemplateView):

    template_name = 'kollektiivi/tag.html'

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Tag, slug=kwargs['slug'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.object
        return context
