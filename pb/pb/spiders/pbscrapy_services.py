
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

class PrivateBankScrapyInsights(CrawlSpider):
    name = "privatebankscraperservices"

    allowed_domains = ["privatebank.jpmorgan.com", "assets.jpmprivatebank.com"]
    start_urls = ["https://privatebank.jpmorgan.com/gl/en/services"]


    rules = (
        Rule(LinkExtractor(allow=[r"/gl/en/services.+", r"https://privatebank.jpmorgan.com/gl/en/services.+"]), callback="parse_services_data", follow= True),
    )

    # def parse(self, response):
    #     links = response.xpath('//a[contains(@class, "jpm-wm-general-headline__cta") or contains(@class, "jpm-wm-general-serviceIcon__bounding-box")]/@href')
    #     for link in links:
    #         url = ""
    #         if("https://privatebank.jpmorgan.com" not in link.get()):
    #             url = "https://privatebank.jpmorgan.com" + link.get()
    #         else:
    #             url = link.get()
    #         yield response.follow(url, callback = self.parse_services_data)

    def parse_services_data(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        selectors = ['div[class*="overview__content"]', 'div[class*="jpm-wm-general-text-overview-hero__wrapper"]', 'div[class="jpm-wm-general-one-up__wrapper"]', 'div[class*="pullquote"]', 'div[class*="rich-text-editor"]', 'div[class*="jpm-wm-general-serviceIcon__wrapper"]']

        str = ""
        for selector in selectors:
            for ele in soup.select(selector):
                str+= ele.get_text("\n", strip=True)


        str
        # print(soup.select('a[class*="-detail-hero__date"]'))
        # print(soup.select('[class*="-detail-hero__author"]'))
        # print(soup.findAll('a[class*="jpm-wm-interactive-tag-row__tag"]'))
        # print(soup.select('[class*="-detail-hero__title"]'))

        yield {
            'url': response.url,
            'pagecontent': str,
            'servicesIncluded': '#'.join([ x.text for x in soup.select('[class*="jpm-wm-general-serviceIcon__bounding-box-title"]')]),
            'title':  [x.text for x in soup.select('[class*="-hero__title"], [class*="overview__title"]')]
        }
        