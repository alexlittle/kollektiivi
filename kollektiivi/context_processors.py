from kollektiivi.models import Page

from kollektiivi.signals import site_tracker


def get_menu(request):
    menu = Page.objects.filter(on_menu=True, active=True).order_by('menu_order_by')
    return {'MENU_ITEMS': menu}


def get_footer(request):
    menu = Page.objects.filter(on_footer=True, active=True).order_by('menu_order_by')
    return {'FOOTER_ITEMS': menu}


def add_analytics(request):
    site_tracker.send(sender=None, request=request)

    return {'site_tracker': True}
