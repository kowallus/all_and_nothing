import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging
import os

logging.getLogger('scrapy').setLevel(logging.WARNING)

class get_pull_reqSpider(scrapy.Spider):
    name = "get_pull_req"

    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 2
    }

    start_urls = [
        'https://github.com/iis-powp-2020/powp_jobs2d/pulls?page=1&q=is%3Aclosed',
        'https://github.com/iis-powp-2020/powp_jobs2d/pulls'
    ]

    def parse_item(self, response):
        # The file name is the same as pull request number
        filename = response.url.split("/")[-1] + '.html'
        foldername = './pull_requests'
        os.makedirs(f'{foldername}', exist_ok=True)
        with open(f'{foldername}/{filename}', 'wb') as f:
            f.write(response.body)

    def parse(self, response):
        print(response.url)

        # parse all pull requests
        for quote in response.xpath('//a[@data-hovercard-type="pull_request"]/@href').getall():
            print(f'Pull request: {quote}')
            yield scrapy.Request(f'https://github.com/{quote}', self.parse_item)

        # check if there is next page
        for quote in response.css('a.next_page::attr(href)').getall():
            print(f'Next page: {quote}')
            yield scrapy.Request(f'https://github.com/{quote}', self.parse)

