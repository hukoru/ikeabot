# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    city = scrapy.Field()
    seq = scrapy.Field()
    parent_place_seq = scrapy.Field()
    parent_place_name = scrapy.Field()

    pass

class PlaceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    nation = scrapy.Field()
    seq = scrapy.Field()

    pass