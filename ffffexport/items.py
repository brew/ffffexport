# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class FfffoundItem(Item):

    title = Field()
    date = Field()
    original_img_url = Field()
    ffffound_img_url = Field()
