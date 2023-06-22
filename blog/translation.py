from modeltranslation.translator import translator, TranslationOptions
from .models import Blog

# for Blog model
class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'body')

translator.register(Blog, BlogTranslationOptions)