# -*- coding: utf-8 -*-

import os
from twisted.internet import task, reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging


configure_logging()


def run_crawl():
    runner = CrawlerRunner(get_project_settings())

    if os.environ.get('NAROU_ID', '') != "" and os.environ.get('NAROU_PW', '') != "":
        runner.crawl('narou')
    if os.environ.get('HAMELN_ID', '') != "" and os.environ.get('HAMELN_PW', '') != "":
        runner.crawl('hameln')


def _main():
    interval = int(os.environ.get('INTERVAL_MINUTES', '30')) * 60
    
    instance = task.LoopingCall(run_crawl)
    instance.start(interval)

    reactor.run()


if __name__ == '__main__':
    _main()