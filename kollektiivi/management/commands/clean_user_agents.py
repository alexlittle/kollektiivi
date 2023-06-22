
"""
Management command to remove bots/crawlers from trackers
"""

import math

from django.core.management.base import BaseCommand

from kollektiivi.models import Tracker
from kollektiivi.lib import search_crawler


class Command(BaseCommand):
    help = "Removes bots/crawlers from trackers"
    block_size = 5000

    def handle(self, *args, **options):
        total_count = Tracker.objects.all().count()
        blocks = math.ceil(total_count/self.block_size)

        for i in range(0, blocks+1):
            start = i*self.block_size
            end = start+self.block_size
            count = 0
            trackers = Tracker.objects.all()[start:end]
            print("checking %d trackers" % trackers.count())
            for tracker in trackers:
                if search_crawler.is_search_crawler(tracker.agent):
                    print("found: " + tracker.agent)
                    tracker.delete()
                    count += 1
            print("Deleted %d in range %d to %d" % (count, start, end))
