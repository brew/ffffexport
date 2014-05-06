# ffffexport

A [Scrapy](http://scrapy.org/) project that downloads images from a ffffound account.

ffffexport attempts to download the original, linked image from a ffffound account. If there's an error retrieving the original, ffffexport will fall back to the archived ffffound image instead.

ffffexport also generates an HTML archive for your browsing pleasure.


## Requirements

ffffexport uses:

* [Scrapy](https://github.com/scrapy/scrapy)
* [Pillow](https://github.com/python-imaging/Pillow)
* [Jinja2](https://github.com/mitsuhiko/jinja2)


## Usage

```
$ scrapy crawl ffffound -a username=<your_username>
```

Images downloaded and HTML is generated in a `/build` directory
