import urlparse

from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector

from ffffexport.items import FfffoundItem


class FfffexportSpider(Spider):
    name = "ffffound"
    allowed_domains = ["ffffound.com"]

    def __init__(self, username, *args, **kwargs):
        super(FfffexportSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://ffffound.com/home/%s/found/" % username]

    def parse(self, response):
        """
        Parse scrapy response objects to yield either FfffoundItem objects or
        new Requests.
        """

        sel = Selector(response)
        assets = sel.css('blockquote.asset')

        for asset in assets:
            item = FfffoundItem()
            description = asset.css('.description::text').extract()
            item['date'] = description[1]
            item['original_img_url'] = [description[0]]
            item['title'] = asset.css('.title a::text').extract()[0]
            item['ffffound_img_url'] = asset.css('table a img[id*=asset]::attr(src)').extract()[0]
            yield item

        try:
            next_url = urlparse.urljoin(response.url, sel.css('#paging-next::attr(href)').extract()[0])
        except IndexError:
            pass
        else:
            yield Request(next_url, callback=self.parse)
