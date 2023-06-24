# signals.py

from django.dispatch import Signal

from kollektiivi.lib import search_crawler

from kollektiivi.models import Tracker


site_tracker = Signal()


def site_tracker_callback(sender, **kwargs):
    request = kwargs.get('request')

    ignore_requests = ['/feed/', '.svg', '.ico']
    ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    agent = request.META.get('HTTP_USER_AGENT', 'unknown')

    if search_crawler.is_search_crawler(agent):
        return

    for i in ignore_requests:
        if request.build_absolute_uri().endswith(i):
            return

    t = Tracker()
    t.url = request.build_absolute_uri()
    t.ip = ip
    t.agent = agent
    t.save()


site_tracker.connect(site_tracker_callback)
