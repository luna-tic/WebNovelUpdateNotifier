# -*- coding: utf-8 -*-

import datetime
import scrapy


class NarouSpider(scrapy.Spider):
    name = 'narou'
    allowed_domains = ['syosetu.com']
    start_urls = ['https://syosetu.com/favnovelmain/isnoticelist/']


    def __init__(self, settings, *args, **kwargs):
        super(NarouSpider, self).__init__(*args, **kwargs)

        self.id = settings.get('NAROU_ID')
        self.pw = settings.get('NAROU_PW')


    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings = crawler.settings)


    def parse(self, response):
        page_title = response.xpath('/html/head/title/text()').get().strip()
        
        if page_title == 'ログイン':
            yield  scrapy.FormRequest.from_response(
                response,
                formxpath='//*[@id="login_box"]/form',
                formdata={'narouid': self.id, 'pass': self.pw},
                callback=self.parse
            )

        elif page_title == '更新通知チェック中一覧':
            for table in response.xpath('//*[@id="main"]/form/table'):
                title = table.xpath('tr[1]/td[2]/a/text()').get().strip()
                author = table.xpath('tr[1]/td[2]/span/text()').get().strip()[1:-1]
                novel_id = table.xpath('tr[1]/td[2]/a/@href').get().strip().split('/')[-2]
                updated_at = datetime.datetime.strptime(table.xpath('tr[2]/td/p[1]/text()').getall()[1].strip()[4:], '%Y/%m/%d %H:%M')
                latest_url = table.xpath('tr[2]/td/p[1]/span[2]/a/@href').get().strip()

                yield {
                    'domain': self.allowed_domains[0],
                    'title': title,
                    'author': author,
                    'novel_id': novel_id,
                    'updated_at': updated_at,
                    'latest_url': latest_url
                }