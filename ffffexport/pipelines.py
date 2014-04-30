import urlparse

from scrapy.http import Request
from scrapy.contrib.pipeline.images import ImagesPipeline


class FfffoundImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # Prefix http:// (missing from scrapped data)
        return [Request(urlparse.urlparse(x, scheme='http').geturl().replace('http:///', 'http://')) for x in item.get(self.IMAGES_URLS_FIELD, [])]
