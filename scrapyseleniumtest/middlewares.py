# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

#from scrapy import signals


#class ScrapyseleniumtestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    #@classmethod
    #def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        #s = cls()
        #crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        #return s

    #def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        #return None

    #def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        #for i in result:
           # yield i

    #def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        #pass

    #def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        #for r in start_requests:
            #yield r

    #def spider_opened(self, spider):
        #spider.logger.info('Spider opened: %s' % spider.name)

from logging import getLogger
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
import time

class ScrapyseleniumtestDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__ (self, chrome_options = None, timeout = None, prefs = None):
        self.prefs = prefs
        self.chrome_options = chrome_options
        self.chrome_options.add_argument('--headless')
        #貌似除了用'prefs'以外，下面这样也可以设置不加载图片：
        #self.chrome_options.add_argument('blink-settings = imagesEnabled = False')
        self.chrome_options.add_experimental_option('prefs', self.prefs)
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = webdriver.Chrome(chrome_options = self.chrome_options)
        self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(timeout = crawler.settings.get('SELENIUM_TIMEOUT'), chrome_options = crawler.settings.get('CHROME_OPTIONS'),
            prefs = crawler.settings.get('PREFS'))

    def process_request(self, request, spider):
        page = request.meta.get('page', 1)
        self.logger.debug('Chrome is processing page %s.' %page)
        try:
            start = time.perf_counter()
            self.browser.get(request.url)
            if page > 1:
                self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(1)
                input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > input')))
                input.clear()
                input.send_keys(page)
                submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > a')))
                submit.click()
                time.sleep(1)
                self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(1)
            else:
                self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(1)
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'), str(page)))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList > ul > li')))
            end = time.perf_counter()
            print('所用时间为：%.10f' %(end - start))
            return HtmlResponse(url = request.url, body = self.browser.page_source, request = request, encoding = 'utf-8', status = 200)
        except TimeoutException:
            return HtmlResponse(url = request.url, request = request, status = 500)

    def __del__(self):
        self.browser.close()
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        #return None

    #def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        #return response

    #def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        #pass

    #def spider_opened(self, spider):
        #spider.logger.info('Spider opened: %s' % spider.name)

