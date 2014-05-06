from cStringIO import StringIO
import urlparse

from PIL import Image

from scrapy import log
from scrapy.http import Request
from scrapy.utils.response import response_status_message
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware


class FfffoundImagesPipeline(ImagesPipeline):
    """
    An image pipeline that adds a fallback_url property to Request.meta dict
    for each image.
    """

    def get_media_requests(self, item, info):
        """
        Include a fallback url (ffffound_img_url) in case the main request url
        fails.
        """

        return [Request(self._prefix_url_scheme(x), meta={'fallback_url': self._prefix_url_scheme(item.get('ffffound_img_url'))})
                    for x in item.get(self.IMAGES_URLS_FIELD, [])]

    def _prefix_url_scheme(self, url):
        """Prefix with 'http://' (missing from scrapped data)."""

        return urlparse.urlparse(url, scheme='http').geturl().replace('http:///', 'http://')


class FfffoundImagesFallBackMiddleware(object):
    """
    Downloader middleware that determines whether images downloaded from the
    FfffoundImagesPipeline have succeeded or whether we need to retry with the
    fallback url.
    """

    def __init__(self, settings):
        self.fallback_http_codes = set(int(x) for x in settings.getlist('FALLBACK_HTTP_CODES'))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_exception(self, request, exception, spider):
        if isinstance(exception, RetryMiddleware.EXCEPTIONS_TO_RETRY) and request.meta.get('fallback_url'):
            log.msg(format="Trying fallback for %(request)s due to exception (fallbackurl is %(fallback_url)s): %(reason)s",
                    level=log.DEBUG, spider=spider, request=request, fallback_url=request.meta.get('fallback_url'), reason=exception)
            return Request(request.meta.get('fallback_url'))

    def process_response(self, request, response, spider):
        # If the request meta dict has a fallback_url property... (only the
        # first original_img_url request has the fallback_url property)
        if request.meta.get('fallback_url') is not None:
            # If the response returned a status code that requires us to use
            # the fallback_url...
            if response.status in self.fallback_http_codes:
                reason = response_status_message(response.status)
                log.msg(format="Trying fallback for %(request)s (fallbackurl is %(fallback_url)s): %(reason)s",
                        level=log.DEBUG, spider=spider, request=request, fallback_url=request.meta.get('fallback_url'), reason=reason)
                return Request(request.meta.get('fallback_url'))
            else:
                # Try to open the image data to check it's valid.
                try:
                    im = Image.open(StringIO(response.body))
                except IOError as e:
                    # use fallback_url if image can't be opened.
                    log.msg(format="Trying fallback for %(request)s (fallbackurl is %(fallback_url)s) because image could not be opened: %(reason)s",
                        level=log.DEBUG, spider=spider, request=request, fallback_url=request.meta.get('fallback_url'), reason=e)
                    return Request(request.meta.get('fallback_url'))
        return response
