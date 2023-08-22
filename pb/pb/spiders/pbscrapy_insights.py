# import scrapy

from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from scrapy import Request

class PrivateBankScrapyInsights(Spider):
    name = "privatebankscraperinsights"

    allowed_domains = ["privatebank.jpmorgan.com", "assets.jpmprivatebank.com"]
    start_urls = ["https://privatebank.jpmorgan.com/gl/en/insights/latest-and-featured"]

    # rules = (
    #     Rule(LinkExtractor(allow=[r"/gl/en/insights.+", r"https://privatebank.jpmorgan.com/gl/en/insights.+"]), callback="parse_insights_data", follow= True),
    # )


    # def parse(self, response):
    #     links = response.xpath('//a[@class="jpm-wm-contentcard__image-link"]/@href')
    #     for link in links:
    #         yield response.follow("https://privatebank.jpmorgan.com" + link.get(), callback = self.parse_insights_data)

    # def parse_insights_data(self, response):
    #     soup = BeautifulSoup(response.body, 'lxml')
    #     selectors = ['span[class*="-detail-hero__tag__link"]', '[class*="-detail-hero__title"]','a[class*="-detail-hero__author"]' , '[class*="-detail-hero__date"]', '[class*="blockquote"]', 'p[class*="__quote"]', 'div[class*="rich-text-editor"]', 'div[class*="single-image__toggle-content"]','div[class*="brightcove-audio__info"]', 'div[class="jpm-wm-general-serviceIcon__wrapper"]', 'span[class="jpm-wm-general-form-container__header--title"]', '[class*="jpm-wm-interactive-tag-row"]','[class*="__video-transcript"]','span[class="jpm-wm-general-form-container__form-summary"]']

    #     str = ""
    #     for selector in selectors:
    #         for ele in soup.select(selector):
    #             if(selector == 'a[class*="-detail-hero__author"]'):
    #                 str += "authors:- "
    #             if(selector == '[class*="-detail-hero__date"]'):
    #                 str += "published Date:- "
    #             str+= ele.get_text("\n", strip=True)

    #     str
    #     # print(soup.select('a[class*="-detail-hero__date"]'))
    #     # print(soup.select('[class*="-detail-hero__author"]'))
    #     # print(soup.findAll('a[class*="jpm-wm-interactive-tag-row__tag"]'))
    #     # print(soup.select('[class*="-detail-hero__title"]'))

    #     yield {
    #         'url': response.url,
    #         'pagecontent': str,
    #         'publishDate': [x.text for x in soup.select('[class*="-detail-hero__date"]')],
    #         'author': [ x.get_text("\n", strip=True) for x in soup.select('[class*="-hero__author"]')],
    #         'tags': [ x.get_text(strip=True) for x in soup.select('a[class*="jpm-wm-interactive-tag-row__tag"]')],
    #         'title':  [x.text for x in soup.select('[class*="-hero__title"], [class*="overview__title"]')]
    #     }
    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        selectors = ['div[class*="text-overview-"]', 'div[class="jpm-wm-general-serviceIcon__wrapper"]', 'div[class="jpm-wm-general-image-embedded__wrapper"]', 'article[class="jpm-wm-contentcard-contentfeed__card"]','span[class="jpm-wm-general-form-container__form-summary"]']
        # selectors = ['//*[h1 or h2 or p or span]']
        str = ""
        for selector in selectors:
            if(selector == 'a[class*="-detail-hero__author"]'):
                str += "authors:-"
            for ele in soup.select(selector):
                str+= ele.get_text("\n", strip=True)
            str= str+"\n"
        yield {
            'url': response.url,
            'pagecontent': str,
            'publishDate': [x.text for x in soup.select('[class*="-detail-hero__date"]')],
            'author': [ x.get_text("\n", strip=True) for x in soup.select('[class*="-hero__author"]')],
            'tags': [ x.get_text(strip=True) for x in soup.select('a[class*="jpm-wm-interactive-tag-row__tag"]')],
            'title':  [x.text for x in soup.select('[class*="-hero__title"], [class*="overview__title"]')]
        }