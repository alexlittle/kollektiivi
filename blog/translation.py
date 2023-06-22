from modeltranslation.translator import translator, TranslationOptions
from .models import Blog

# forBlog model
class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'menu_title', 'body')



translator.register(Page, PageTranslationOptions)
translator.register(Tag, TagTranslationOptions)