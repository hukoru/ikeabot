# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import datetime
from crow.items import ProductItem
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.http import FormRequest
from scrapy.selector import Selector

import sys, os

#url = "http://eng.lottedfs.com/handler/Category-Main?categoryId=8000510013&tracking=LNB_ACC_1"



class PlaceSpider(scrapy.Spider):
    name = "shilla_product_spider"

    allowed_domains = ["www.shilladfs.com"]
    #start_urls = [url]

    def start_requests(self):
        return [ FormRequest("http://www.shilladfs.com/category/categoryList.dfs?catgLevel=2&dispCatgId=23",
                     formdata={'affl_id': '',
                               'sAll': '',
                               'isBrand': '',
                               'collection': 'item',
                               'sortOrder': 'DESC',
                               'sortValue': 'accum_sale_qty',
                               'startCount': '0',
                               'listCount': '100',
                               'viewType': 'list',
                               'sendType': 'category',
                               'catgLevel': '2',
                               'dispCatgId': '23',
                               'dispCatgName': '선글라스',
                               'brand_id': '',
                               'requery': '',
                               'searchField': 'ALL',
                               'query': '',
                               'category': '',
                               'categoryName': '',
                               'fir_min_price': '0',
                               'fir_max_price': '999999999999',
                               'max_price': '999999999999',
                               'min_price': '0',
                               'searchArea': '1',
                               'inputMin': '0',
                               'inputMax': '999999999999'
                     },
                     callback=self.parse) ]


    def parse(self, response):

        try:

            hxs = HtmlXPathSelector(response)
            create_date = datetime.datetime.now().strftime('%Y%m%d')

            places = hxs.select("//div[@class='prlisttypewrap']/ul/li")

            for place in places:
                item = ProductItem()
                sid = "shilla"
                code = place.select("div/a[1]/@href").extract()[0]
                ref_code = place.select("div/div[1]/dl/dd/text()").extract()[0]

                name = place.select("div/div[1]/dl/dd/text()").extract()[0]

                print ref_code


                image_url = place.select("div/a/img/@src").extract()[0]

                brand_name = place.select("div/div[1]/a/text()").extract()[0]
                brand_code = place.select("div/div[1]/a/@href").extract()[0]

                code_value = re.search("javascript:viewProdDetl\('(.*?)'", code)
                brand_code_value = re.search("javascript:viewProdDetl\('(.*?)'", brand_code)

                price = place.select("div/div[@class='price']/strong/text()").extract()[0]
                price_won = place.select("div/div[@class='price']/span/text()").extract()[0]

                item['name'] = name
                item['code'] = code_value.group(1)
                item['ref_code'] = ref_code
                item['price'] = price
                item['image_url'] = image_url
                item['price_won'] = price_won
                item['brand_name'] = brand_name
                item['brand_code'] = brand_code_value.group(1)
                item['sid'] = sid
                item['create_date'] = create_date

                yield item








        except:
            print "insert failed", sys.exc_info()