# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from urllib.parse import quote
from scrapyseleniumtest.items import ProductItem


class JingdongSpider(Spider):
    name = 'jingdong'
    allowed_domains = ['www.jd.com']
    base_url = 'https://search.jd.com/Search?keyword='

    def start_requests(self):
    	for keyword in self.settings.get('KEYWORDS'):
    		for page in range(1, self.settings.get('MAX_PAGE') + 1):
    			url = self.base_url + quote(keyword) + '&enc=utf-8'
    			yield Request(url = url, callback = self.parse, meta = {'page': page}, dont_filter = True)

    def parse(self, response):
        products = response.xpath('//*[@id="J_goodsList"]/ul/li')
        for product in products:
        	item = ProductItem()
        	item['title'] = ''.join(product.xpath('./div/div[3]/a/em/text()').extract()).strip()
        	item['price'] = ''.join(product.xpath('./div/div[2]/strong//text()').extract()).strip()
        	item['shop'] = product.xpath('./div/div[5]/span/a/@title').extract_first()
        	item['comments'] = ''.join(product.xpath('./div/div[4]/strong//text()').extract()).strip()
        	item['url'] = product.xpath('./div/div[1]/a/@href').extract_first()
        	yield item