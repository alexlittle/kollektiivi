from modeltranslation.translator import register, translator, TranslationOptions
from .models import Post, PostAttachment

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'body')

@register(PostAttachment)
class PostAttachmentTranslationOptions(TranslationOptions):
    fields = ('title',)

