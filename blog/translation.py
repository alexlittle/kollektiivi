from modeltranslation.translator import register, translator, TranslationOptions
from .models import Post

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'body')

