
from modeltranslation.translator import register, translator, TranslationOptions
from .models import Page, Tag, Member


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'body')


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Member)
class MemberTranslationOptions(TranslationOptions):
    fields = ('name', 'body', 'contact')
