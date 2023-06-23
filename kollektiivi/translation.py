
from modeltranslation.translator import register, translator, TranslationOptions
from .models import Page, Tag, Member

# for Page model
@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'body')

# for Tag model
@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

# for Member model
@register(Member)
class MemberTranslationOptions(TranslationOptions):
    fields = ('name', 'body')

