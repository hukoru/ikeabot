# -*- coding: utf-8 -*-
import scrapy
import requests
from crow.items import PlaceItem
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.selector import Selector

import sys, os

url = "http://www.ratebeer.com/places/browse/"

class PlaceSpider(scrapy.Spider):
    name = "places_spider"

    allowed_domains = ["www.ratebeer.com"]
    start_urls = [url]


    def parse(self, response):

        try:

            hxs = HtmlXPathSelector(response)

            #United States, England, Germany, Canada places 크롤링
            places = hxs.select("//div[@id='container']/div/table/tr[1]/td/table/tr[2]/td/a")

            #print places_links.extract()

            print len(places)

            for place in places:
                item = PlaceItem()
                title = place.select("text()")[0].extract()
                title = title.rstrip()
                url = place.select("@href")[0].extract()


                urls = url.split("/")
                urlType = len(urls)

                item['title'] = title
                item['url'] = url

                #미국 url
                if urlType == 5:

                    item['nation'] = urls[2]
                    item['seq'] = urls[3]

                #영국 url
                if urlType == 7:
                    item['nation'] = urls[2]
                    item['seq'] = urls[5]

                #독일, 캐나다 url
                if urlType == 6:
                    item['nation'] = urls[2]
                    item['seq'] = urls[4]


                yield item

            #Global
            places = hxs.select("//div[@id='container']/div/table/tr[2]/td/table/tr[2]/td/a")

            #print places

            for place in places:
                item = PlaceItem()
                title = place.select("text()")[0].extract()
                title = title.rstrip()
                url = place.select("@href")[0].extract()

                nation = url.split("/")

                item['title'] = title
                item['url'] = url
                item['nation'] = nation[2]
                item['seq'] = nation[3]

                yield item



        except:
            print "insert failed", sys.exc_info()[0]