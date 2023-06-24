from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from kollektiivi.models import Page, Tag, Member
from blog import utils


class HomeView(TemplateView):

    template_name = 'kollektiivi/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['page'] = get_object_or_404(Page, slug='etusivu')
        context['news'] = utils.get_posts(3)
        context['members'] = Member.objects.filter(active=True)
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


class MembersView(TemplateView):

    template_name = 'kollektiivi/members.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members_current'] = Member.objects.filter(active=True)
        context['members_previous'] = Member.objects.filter(active=False)
        return context


class MemberProfileView(TemplateView):

    template_name = 'kollektiivi/member-profile.html'

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Member, slug=kwargs['slug'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member'] = self.object
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
