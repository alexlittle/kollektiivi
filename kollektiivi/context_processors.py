from kollektiivi.models import Page, Member

from kollektiivi.signals import site_tracker


def get_menu(request):
    menu = Page.objects.filter(on_menu=True, active=True)
    members = Member.objects.filter(active=True)
    return {'MENU_ITEMS': menu,
            'MEMBERS': members}


def get_footer(request):
    menu = Page.objects.filter(on_footer=True, active=True)
    return {'FOOTER_ITEMS': menu}


def add_analytics(request):
    site_tracker.send(sender=None, request=request)

    return {'site_tracker': True}
