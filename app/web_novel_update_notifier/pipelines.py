# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import os
import json
import sqlite3
import contextlib
import requests


DB_PATH = 'db.sqlite3'
TABLE_NAME = 'novels'


class WebNovelUpdateNotifierPipeline(object):
    def __init__(self, settings, *args, **kwargs):
        super(WebNovelUpdateNotifierPipeline, self).__init__(*args, **kwargs)

        self.slack_url = settings.get('SLACK_URL')
        self.slack_channel = settings.get('SLACK_CHANNEL')
        self.slack_bot_name = settings.get('SLACK_BOT_NAME')
        self.slack_bot_icon = settings.get('SLACK_BOT_ICON')


    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings = crawler.settings)


    def process_item(self, item, spider):
        if self.novel_exists(item):
            if self.is_updated(item):
                self.update_novel(item)
                self.notify_slack(item)
        else:
            self.insert_novel(item)

        return item


    @contextlib.contextmanager
    def open_db(self):
        db = sqlite3.connect(
            os.path.join(os.getcwd(), DB_PATH))

        cursor = db.cursor()
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}(\
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                domain TEXT NOT NULL, \
                novel_id TEXT NOT NULL, \
                title TEXT NOT NULL, \
                author TEXT, \
                latest_url TEXT NOT NULL, \
                updated_at DATE \
            );')

        try:
            yield  db
        finally:
            db.close()


    def insert_novel(self, item):
        with self.open_db() as db:
            db.execute(
                f'INSERT INTO {TABLE_NAME} (domain, novel_id, title, author, latest_url, updated_at) VALUES (?, ?, ?, ?, ?, ?)', (
                    item['domain'],
                    item['novel_id'],
                    item['title'],
                    item['author'],
                    item['latest_url'],
                    item['updated_at'],
                )
            )
            db.commit()
            logging.info(f'Insert {item}')


    def update_novel(self, item):
        with self.open_db() as db:
            db.execute(
                f'UPDATE {TABLE_NAME} SET title=?, author=?, latest_url=?, updated_at=? WHERE domain=? AND novel_id=?',
                (item['title'], item['author'], item['latest_url'], item['updated_at'], item['domain'], item['novel_id'],)
            )
            db.commit()
            logging.info(f'Update {item}')


    def novel_exists(self, item):
        with self.open_db() as db:
            cursor = db.execute(
                f'SELECT * FROM {TABLE_NAME} WHERE domain=? AND novel_id=?',
                (item['domain'], item['novel_id'],)
            )
            return True if cursor.fetchone() else False


    def is_updated(self, item):
        with self.open_db() as db:
            cursor = db.execute(
                f'SELECT * FROM {TABLE_NAME} WHERE domain=? AND novel_id=?',
                (item['domain'], item['novel_id'],)
            )
            
            return cursor.fetchone()[5] != item['latest_url']


    def notify_slack(self, item):
        fields = []
        fields += [{'title': 'Author', 'value': item['author'], 'short': True}]
        fields += [{'title': 'Updated', 'value': item['updated_at'].strftime('%Y/%m/%d %H:%M'), 'short': True}]
        
        attachments = [{'fallback': f'{item["title"]} is updated', 'title': item['title'], 'title_link': item['latest_url'], 'fields': fields}]

        payload = {'username': self.slack_bot_name, 'icon_emoji': self.slack_bot_icon, 'attachments': attachments}

        if self.slack_channel:
            payload['channel'] = self.slack_channel

        requests.post(self.slack_url, json.dumps(payload))
