# -*- coding: utf-8 -*-
import scrapy
import requests
from crow.items import ProductItem
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.http import FormRequest
from scrapy.selector import Selector

import sys, os

#url = "http://eng.lottedfs.com/handler/Category-Main?categoryId=8000510013&tracking=LNB_ACC_1"

class PlaceSpider(scrapy.Spider):
    name = "category_spider"

    allowed_domains = ["www.lottedfs.com"]
    #start_urls = [url]

    def start_requests(self):
        return [ FormRequest("http://www.lottedfs.com/handler/Category-Main",
                     formdata={'categoryId': '1000510013',
                               'sOrderBy': '1',
                               'pageNo': '1',
                               'option': '',
                               'vType': 'list',
                               'selChg': '1',
                               'SelectedBrandCdList': '',
                               'SelectedBrandNmList': '',
                               'CategoryBrandLayerVal': '',
                               'minprice': '23',
                               'maxprice': '792',
                               'listCount': '50'
                     },
                     callback=self.parse) ]



    def parse(self, response):

        try:

            hxs = HtmlXPathSelector(response)

            places = hxs.select("//table[@class='prodImg02']/tbody/tr")

            print len(places)

            for place in places:
                item = ProductItem()
                name = place.select("td[@class='ln']/p[@class='name']/a/text()").extract()[0]
                code = place.select("td[@class='ln']/p[@class='code']/a/@href").extract()[0]

                price = place.select("td[4]/p[2]/text()").extract()[0]
                price_won = place.select("td[4]/span/text()").extract()[0]

                item['name'] = name
                item['code'] = code[31:-9]
                item['price'] = price
                item['price_won'] = price_won

                #item['title'] = title
                yield item

            #상위 카테고리명  ////*[@id="allProductsContainer"]
            #upper_categorys_titles = start_hxs.select("div[1]")
            #print len(categorys.select("div/span/text()").extract())

            #print categorys.select("div/span/text()").extract()


                #title = place.select("text()")[0].extract()
                #title = title.rstrip()
               # url = place.select("@href")[0].extract()

            #//*[@id="allProductsContainer"]/div[2]/div[1]

                #//*[@id="allProductsContainer"]/div[2]/div[1]/div
                #//*[@id="allProductsContainer"]/div[2]/div[1]/div

            #//*[@id="allProductsContainer"]/div[2]

            #United States, England, Germany, Canada places 크롤링




        except:
            print "insert failed", sys.exc_info()