
from modeltranslation.translator import translator, TranslationOptions
from .models import Page, Tag

# for Page model
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'menu_title', 'body')

# for Tag model
class TagTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


translator.register(Page, PageTranslationOptions)
translator.register(Tag, TagTranslationOptions)
