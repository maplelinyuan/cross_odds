# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import datetime, time
import pdb
from twilio.rest import Client
import traceback
import requests

class CrossoddsPipeline(object):
    def __init__(self):
        # 链接数据库
        self.mongo_client = MongoClient(host='localhost', port=27019)
        # self.mongo_client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])     #如果有账户密码

    def process_item(self, item, spider):
        db_name = 'cross_odds'
        self.db = self.mongo_client[db_name]  # 获得数据库的句柄
        company_name = item['company_name']
        league_name = item['league_name']
        match_id_1 = item['match_id_1']
        match_id_2 = item['match_id_2']
        col_name = 'qiutan_realtime'
        self.coll = self.db[col_name]  # 获得collection的句柄
        try:
            # 如果col_name（集合名称） 在 该数据中，则使用update更新，否则insert
            if not self.coll.find({'company_name': company_name, 'match_id_1': match_id_1, 'match_id_2':match_id_2}).count() > 0:
                match_1_home_name = item['match_1_home_name']
                match_1_away_name = item['match_1_away_name']
                match_1_match_time = item['match_1_match_time']
                match_1_home_odd = item['match_1_home_odd']
                match_1_draw_odd = item['match_1_draw_odd']
                match_1_away_odd = item['match_1_away_odd']
                match_2_home_name = item['match_2_home_name']
                match_2_away_name = item['match_2_away_name']
                match_2_match_time = item['match_2_match_time']
                match_2_home_odd = item['match_2_home_odd']
                match_2_draw_odd = item['match_2_draw_odd']
                match_2_away_odd = item['match_2_away_odd']
                insertItem = dict(company_name=company_name, league_name=league_name, match_id_1=match_id_1, match_id_2=match_id_2,
                                  match_1_home_name=match_1_home_name, match_1_away_name=match_1_away_name, match_1_match_time=match_1_match_time,
                                  match_1_home_odd=match_1_home_odd, match_1_draw_odd=match_1_draw_odd, match_1_away_odd=match_1_away_odd,
                                  match_2_home_name=match_2_home_name, match_2_away_name=match_2_away_name, match_2_match_time=match_2_match_time,
                                  match_2_home_odd=match_2_home_odd, match_2_draw_odd=match_2_draw_odd, match_2_away_odd=match_2_away_odd)
                self.coll.insert(insertItem)

        except Exception as err:
            print('%s\n%s' % (err, traceback.format_exc()))
        finally:
            self.mongo_client.close()
        return item
