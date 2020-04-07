import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging
import os

logging.getLogger('scrapy').setLevel(logging.WARNING)

class get_fork_pull_reqSpider(scrapy.Spider):
    name = "get_fork_pull_req"

    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOAD_DELAY': 2
    }

    start_urls = [
        'https://github.com/iis-io-team/pio_git_rhymers/network/members'
    ]

    def parse_item(self, response):
        # The file name is the same as pull request number
        print(f'writing: {response.url}')
        rootname = './pio_git_rhymers'
        membername = response.url.split("/")[-4]
        filename = response.url.split("/")[-1] + '.html'
        foldername = 'pull_requests'
        os.makedirs(f'{rootname}', exist_ok=True)
        os.makedirs(f'{rootname}/{membername}', exist_ok=True)
        os.makedirs(f'{rootname}/{membername}/{foldername}', exist_ok=True)
        with open(f'{rootname}/{membername}/{foldername}/{filename}', 'wb') as f:
            f.write(response.body)

    def parse_fork_pulls(self, response):
        print(response.url)

        # parse all pull requests
        for quote in response.xpath('//a[@data-hovercard-type="pull_request"]/@href').getall():
            print(f'Pull request: {quote}')
            yield scrapy.Request(f'https://github.com/{quote}', self.parse_item)

        # check if there is next page
        for quote in response.css('a.next_page::attr(href)').getall():
            print(f'Next page: {quote}')
            yield scrapy.Request(f'https://github.com/{quote}', self.parse_fork_pulls)


    def parse(self, response):
        print(response.url)

        # parse all fork repos
        for quote in response.xpath('//a/@href').getall():
            if '/pio_git_rhymers' in str(quote) and '/iis-io-team/' not in str(quote):
                print(f'Fork repo: {quote}')
                yield scrapy.Request(f'https://github.com/{quote}/pulls', self.parse_fork_pulls)
                yield scrapy.Request(f'https://github.com/{quote}/pulls?page=1&q=is%3Aclosed', self.parse_fork_pulls)


