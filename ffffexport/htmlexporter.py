from math import ceil
import os

from scrapy.conf import settings
from scrapy import signals
from scrapy.exceptions import NotConfigured

from jinja2 import Environment, PackageLoader


class HTMLExporter(object):

    def __init__(self):
        self.items = []

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('HTMLEXPORTER_ENABLED'):
            raise NotConfigured

        exporter = cls()
        crawler.signals.connect(exporter.spider_opened, signals.spider_opened)
        crawler.signals.connect(exporter.spider_closed, signals.spider_closed)
        crawler.signals.connect(exporter.item_scraped, signals.item_scraped)
        return exporter

    def spider_opened(self, spider):
        print("spider opened!")

    def spider_closed(self, spider, reason):
        if reason == 'finished':
            # the spider has closed normally, write the items to html!
            env = Environment(loader=PackageLoader('ffffexport', 'templates'))
            template = env.get_template('page.html')

            items_per_page = settings.get('HTMLEXPORTER_ITEMS_PER_PAGE', 20)
            number_of_pages = int(ceil(len(self.items) / float(items_per_page)))

            # A list containing tuples in the form:
            # [(<page number>, <page url>), ... ]
            pagination = []
            for i in range(1, number_of_pages + 1):
                pagination.append((i, self._make_page_url(i)))

            for page_num in range(number_of_pages):
                html_file_path = self._make_page_url(page_num + 1)
                start_items = items_per_page * page_num
                end_items = start_items + items_per_page

                with open(html_file_path, 'w+') as html_file:
                    context = {
                        'items': self.items[start_items:end_items],
                        'current_page': page_num + 1,
                        'total_pages': number_of_pages,
                        'pagination': pagination,
                    }
                    html_file.write(template.render(context).encode("UTF-8"))

    def item_scraped(self, item, response, spider):
        self.items.append({'title': item['title'], 'path': 'images/%s' % item['images'][0]['path']})
        return item

    def _make_page_url(self, page_num):
        return os.path.join(settings['BUILD_DIR'], '%s.html' % "{0:04d}".format(page_num))
