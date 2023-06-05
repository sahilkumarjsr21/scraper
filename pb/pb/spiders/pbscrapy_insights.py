# import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

class PrivateBankScrapyInsights(CrawlSpider):
    name = "privatebankscraperinsights"

    allowed_domains = ["privatebank.jpmorgan.com", "assets.jpmprivatebank.com"]
    start_urls = ["https://privatebank.jpmorgan.com/gl/en/insights"]

    rules = (
        Rule(LinkExtractor(allow=[r"/gl/en/insights.+", r"https://privatebank.jpmorgan.com/gl/en/insights.+"]), callback="parse_insights_data", follow= True),
    )

    # def parse(self, response):
    #     links = response.xpath('//a[@class="jpm-wm-contentcard__image-link"]/@href')
    #     for link in links:
    #         yield response.follow("https://privatebank.jpmorgan.com" + link.get(), callback = self.parse_insights_data)

    def parse_insights_data(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        selectors = ['span[class*="-detail-hero__tag__link"]', '[class*="-detail-hero__title"]','a[class*="-detail-hero__author"]' , '[class*="-detail-hero__date"]', '[class*="blockquote"]', 'p[class*="__quote"]', 'div[class*="rich-text-editor"]', 'div[class*="single-image__toggle-content"]','div[class*="brightcove-audio__info"]', 'div[class="jpm-wm-general-serviceIcon__wrapper"]', 'span[class="jpm-wm-general-form-container__header--title"]', 'a[class*="jpm-wm-interactive-tag-row__tag"]','span[class="jpm-wm-general-form-container__form-summary"]', '[class*="__video-transcript"]']

        str = ""
        for selector in selectors:
            for ele in soup.select(selector):
                if(selector == 'a[class*="-detail-hero__author"]'):
                    str += "authors:- "
                if(selector == '[class*="-detail-hero__date"]'):
                    str += "published Date:- "
                str+= ele.get_text("\n", strip=True)

        str
        # print(soup.select('a[class*="-detail-hero__date"]'))
        # print(soup.select('[class*="-detail-hero__author"]'))
        # print(soup.findAll('a[class*="jpm-wm-interactive-tag-row__tag"]'))
        # print(soup.select('[class*="-detail-hero__title"]'))

        yield {
            'url': response.url,
            'pagecontent': str,
            'publishDate': [x.text for x in soup.select('[class*="-detail-hero__date"]')],
            'author': '#'.join([ x.text for x in soup.select('[class*="-hero__author"]')]),
            'tags': '#'.join([ x.text for x in soup.select('a[class*="jpm-wm-interactive-tag-row__tag"]')]),
            'title':  [x.text for x in soup.select('[class*="-hero__title"], [class*="overview__title"]')]
        }
        