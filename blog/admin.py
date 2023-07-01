
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('display_date', 'title', 'title_fi', 'title_en', 'slug', 'active', 'show_preview_url', 'hit_count')
    search_fields = ['title', 'body', 'slug']
    ordering = ['-display_date', 'title']
    readonly_fields=('created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs

    def show_preview_url(self, obj):
        return format_html("<a href="
                           + reverse('blog:post',
                                     args={obj.slug})
                           + "?preview=1>"
                           + obj.title
                           + " - preview</a>")

    def hit_count(self, obj):
        return obj.get_hits()

    show_preview_url.short_description = "Preview"
    hit_count.short_description = "Hit count"


admin.site.register(Post, PostAdmin)
