# -*- coding: utf-8 -*-

import datetime
import scrapy


class HamelnSpider(scrapy.Spider):
    name = 'hameln'
    allowed_domains = ['syosetu.org']
    start_urls = ['https://syosetu.org/?mode=favo']


    def __init__(self, settings, *args, **kwargs):
        super(HamelnSpider, self).__init__(*args, **kwargs)

        self.id = settings.get('HAMELN_ID')
        self.pw = settings.get('HAMELN_PW')


    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings = crawler.settings)


    def parse(self, response):
        page_title = response.xpath('/html/head/title/text()').get().strip()

        if page_title == 'ログイン - ハーメルン':
            yield  scrapy.FormRequest.from_response(
                response,
                formxpath='//*[@id="main"]/div/form',
                formdata={'id': self.id, 'pass': self.pw},
                callback=self.parse
            )

        elif page_title == 'マイページ - ハーメルン':
            yield scrapy.Request(self.start_urls[0], callback=self.parse)

        elif page_title == 'お気に入り - ハーメルン':
            for table in response.xpath('//*[@id="main"]/div[2]/form/div'):
                title = table.xpath('h3/a[1]/text()').get().strip()
                author_link = table.xpath('h3/a[2]/text()')
                if author_link:
                    author = author_link.get().strip()
                else:
                    author = table.xpath('h3/text()').getall()[1].strip()[4:-1]
                novel_id = table.xpath('h3/a[1]/@href').get().strip().split('/')[-2]
                temp = table.xpath('p[2]/text()').get().strip()
                updated_at = datetime.datetime.strptime(temp[:11] + temp[15:], '%Y年%m月%d日%H:%M')
                latest_url = table.xpath('p[2]/a[1]/@href').get().strip()

                yield {
                    'domain': self.allowed_domains[0],
                    'title': title,
                    'author': author,
                    'novel_id': novel_id,
                    'updated_at': updated_at,
                    'latest_url': latest_url
                }