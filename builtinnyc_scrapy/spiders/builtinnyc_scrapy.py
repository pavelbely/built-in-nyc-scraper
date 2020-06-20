__author__ = 'Pavel Bely'

from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.selector import Selector
from builtinnyc_scrapy.items import CompanyItem


class BuiltInNycSpider(CrawlSpider):
    """
    This CrawlSpider will look into the specific city and pull out content for
    Title, Ad's URL, Post Date, Post Date Specific (i.e. datetime), Price,
    Room Details, and Locations. Please reference https://sites.google.com/site/clsiteinfo/city-site-code-sort
    for more on city codes and link.

    If you need to change the city code, please do so at the three locations below:
    allowed domains, start urls, and rules.

    Feel free to change the name of the spider to something more specific.

    """
    name = 'builtinnyc'
    allowed_domains = ['builtinnyc.com']
    start_urls = ['https://www.builtinnyc.com/companies?f%5B0%5D=company_types_aggregate_type_industry%3A79&f%5B1%5D=company_types_aggregate_type_industry%3A66&page=13']

    next_page_url = r'company_types_aggregate_type_industry%3A66&page=\d+$'
    rules = (
        # Rule(LxmlLinkExtractor(
        #         allow=(next_page_url),
        #     ),
        #     # callback="parse_next_page",
        #     # follow=True,
        # ),
        Rule(LxmlLinkExtractor(
                allow=(
                    r'https://www.builtinnyc.com/company/[\w-]+$'
                ),
                restrict_xpaths="//div[contains(@class, 'company-filtered-card')]"
            ),
            callback="parse_item",
            follow=True,
        ),
        # Rule(LxmlLinkExtractor(allow=("search/apa?s=d00&")), callback="parse_items_2", follow= True),
        )

    def parse_next_page(self, response):
        """
            This function takes the content from contents and map them according to the
            items from items.py. If the key exists in content, then Scrapy will aggregate
            the rest of the items and combine them.

            Each content will have "[0]" to indicate the first listing from the array.
        """
        self.logger.info('You are now crawling: %s', response.url)

    def parse_item(self, response):
        """
        This function takes teh content from contents and map them according to the
        items from items.py. If the key exists in content, then Scrapy will aggregate
        the rest of the items and combine them.

        Each content will have "[0]" to indicate the first listing from the array.
        """
        self.logger.info('You are now crawling: %s', response.url)
        item = CompanyItem()
        item['title'] = response.xpath("//div[@class='company-card-title']/h1/text()").extract_first()
        website_str = response.xpath("//div[@class='item item-website' or @class='item website']/a/@href").extract_first() or ''
        item["website"] = website_str.replace('?utm_source=BuiltinNYC', '').rstrip('/')
        item["builtin_url"] = response.url
        yield item
