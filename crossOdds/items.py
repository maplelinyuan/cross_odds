# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrossoddsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field()
    league_name = scrapy.Field()
    match_id_1 = scrapy.Field()
    match_1_home_name = scrapy.Field()
    match_1_away_name = scrapy.Field()
    match_1_match_time = scrapy.Field()
    match_1_home_odd = scrapy.Field()
    match_1_draw_odd = scrapy.Field()
    match_1_away_odd = scrapy.Field()
    match_id_2 = scrapy.Field()
    match_2_home_name = scrapy.Field()
    match_2_away_name = scrapy.Field()
    match_2_match_time = scrapy.Field()
    match_2_home_odd = scrapy.Field()
    match_2_draw_odd = scrapy.Field()
    match_2_away_odd = scrapy.Field()
