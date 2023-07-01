from django.contrib import admin

from kollektiivi.models import Tracker, Page, Tag, Member


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_en', 'title_fi', 'slug', 'menu_order_by', 'on_menu', 'on_footer', 'active')
    search_fields = ['title', 'slug', 'body']
    readonly_fields=('created_by', 'updated_by')
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'name_fi', 'slug')


class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'name_fi', 'slug', 'active', 'visible')
    readonly_fields=('created_by', 'updated_by')
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class TrackerAdmin(admin.ModelAdmin):
    list_display = ('tracker_date', 'ip', 'url', 'agent')


admin.site.register(Page, PageAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Tracker, TrackerAdmin)
admin.site.register(Member, MemberAdmin)
