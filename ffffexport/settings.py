# Scrapy settings for ffffexport project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os


BOT_NAME = 'ffffexport'

SPIDER_MODULES = ['ffffexport.spiders']
NEWSPIDER_MODULE = 'ffffexport.spiders'
BUILD_DIR = os.path.join(os.path.dirname(__file__), '../build/')

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'ffffexport (+http://www.yourdomain.com)'

ITEM_PIPELINES = {'ffffexport.pipelines.FfffoundImagesPipeline': 1}
IMAGES_STORE = os.path.join(BUILD_DIR, 'images/')
IMAGES_URLS_FIELD = "original_img_url"

EXTENSIONS = {
    'ffffexport.htmlexporter.HTMLExporter': 500,
}

# Enabling the HTMLExporter extention will write items to html files for easy
# browsing.
HTMLEXPORTER_ENABLED = True
HTMLEXPORTER_ITEMS_PER_PAGE = 10
