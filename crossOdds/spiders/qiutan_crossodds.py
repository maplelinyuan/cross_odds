# -*- coding: utf-8 -*-
import scrapy
import pdb
from crossOdds.items import CrossoddsItem
from scrapy_splash import SplashRequest
from crossOdds.spiders.tools import MyTools
from scrapy_redis.spiders import RedisSpider
from pymongo import MongoClient
import traceback
import time
import redis

# scrapy crawl crossOdds
# class QiutanCrossoddsSpider(scrapy.Spider):
class OriginOddsSpider(RedisSpider):
    name = 'qiutan_crossodds'
    allowed_domains = ['http://op1.win007.com/']
    start_urls = []
    redis_key = 'qiutan_crossodds:start_urls'
    global splashurl
    splashurl = "http://192.168.99.100:8050/render.html"

    # 此处是重父类方法，并使把url传给splash解析
    def make_requests_from_url(self, url):
        global splashurl
        url = splashurl + "?url=" + url
        # 使用代理访问
        proxy = MyTools.get_proxy()
        LUA_SCRIPT = """
                                function main(splash)
                                    splash:on_request(function(request)
                                        request:set_proxy{
                                            host = "%(host)s",
                                            port = %(port)s,
                                            username = '', password = '', type = "HTTPS",
                                        }
                                        request:set_header('X-Forwarded-For', %(proxy_ip)s)
                                    end)
                                    assert(splash:go(args.url))
                                    assert(splash:wait(1))
                                    return {
                                        html = splash:html(),
                                    }
                                end
                                """
        try:
            proxy_host = proxy.strip().split(':')[0]
            proxy_port = int(proxy.strip().split(':')[-1])
            LUA_SCRIPT = LUA_SCRIPT % {'host': proxy_host, 'port': proxy_port, 'proxy_ip': proxy_host}
            print('make_requests代理为：', "http://{}".format(proxy))
            return SplashRequest(url, self.parse,
                                 args={'wait': 0.5, 'images': 0, 'timeout': 30, 'lua_source': LUA_SCRIPT},
                                 dont_filter=True)
        except Exception as err:
            MyTools.delete_proxy(proxy)
            print('%s\n%s' % (err, traceback.format_exc()))

    def start_requests(self):
        for url in self.start_urls:
            proxy = MyTools.get_proxy()

            LUA_SCRIPT = """
                                    function main(splash)
                                        splash:on_request(function(request)
                                            request:set_proxy{
                                                host = "%(host)s",
                                                port = %(port)s,
                                                username = '', password = '', type = "HTTPS",
                                            }
                                            request:set_header('X-Forwarded-For', %(proxy_ip)s)
                                        end)
                                        assert(splash:go(args.url))
                                        assert(splash:wait(1))
                                        return {
                                            html = splash:html(),
                                        }
                                    end
                                    """
            proxy_host = proxy.strip().split(':')[0]
            proxy_port = int(proxy.strip().split(':')[-1])
            LUA_SCRIPT = LUA_SCRIPT % {'host': proxy_host, 'port': proxy_port, 'proxy_ip': proxy_host}
            try:
                yield SplashRequest(url, self.parse, args={'wait': 0.5, 'images': 0, 'timeout': 30, 'lua_source': LUA_SCRIPT}, dont_filter=True)
            except Exception as err:
                print('%s\n%s' % (err, traceback.format_exc()))
    #
    # '''
    #     redis中存储的为set类型的公司名称，使用SplashRequest去请求网页。
    #     注意：不能在make_request_from_data方法中直接使用SplashRequest（其他第三方的也不支持）,会导致方法无法执行，也不抛出异常
    #     但是同时重写make_request_from_data和make_requests_from_url方法则可以执行
    # '''

    def parse(self, response):
        try:
            trs = response.xpath('//table[@id="table_schedule"]/tbody/tr')
            company_name = response.url.split('=')[-1]
            total_arr = {}
            for tr in trs:
                if len(tr.xpath('td')) != 13 or len(tr.xpath('td')[0].xpath('text()')) > 0:
                    continue
                if len(tr.xpath('td')[1].xpath('a').extract()) > 0:
                    league_name = tr.xpath('td')[1].xpath('a/text()').extract()[0]
                else:
                    league_name = tr.xpath('td')[1].xpath('text()').extract()[0]
                print(league_name)
                home_name = tr.xpath('td')[3].xpath('a/text()').extract()[0].split(' ')[0]
                away_name = tr.xpath('td')[11].xpath('a/text()').extract()[0].split(' ')[0]
                match_time = '20' + tr.xpath('td')[2].xpath('text()').extract()[0] + ' ' + tr.xpath('td')[2].xpath('text()').extract()[1]
                match_id = tr.xpath('td')[4].xpath('@onclick').extract()[0].split('(')[1].split('&')[0].split("'")[1]
                home_odd = float(tr.xpath('td')[4].xpath('text()').extract()[0])
                draw_odd = float(tr.xpath('td')[5].xpath('text()').extract()[0])
                away_odd = float(tr.xpath('td')[6].xpath('text()').extract()[0])
                current_info = dict(match_id=match_id, match_time=match_time, home_name=home_name, away_name=away_name, home_odd=home_odd, draw_odd=draw_odd, away_odd=away_odd)
                if league_name in total_arr:
                    # 判断之前的同league比赛是否有赔率相等的
                    for pre_info in total_arr[league_name]:
                        pre_home_odd = pre_info['home_odd']
                        pre_draw_odd = pre_info['draw_odd']
                        pre_away_odd = pre_info['away_odd']
                        if draw_odd == pre_draw_odd and ((home_odd == pre_home_odd and away_odd == pre_away_odd) or (home_odd == pre_away_odd and away_odd == pre_draw_odd)):
                            # 找到相同的两组, 存储数据
                            single_pair_item = CrossoddsItem()
                            single_pair_item['company_name'] = company_name
                            single_pair_item['league_name'] = league_name
                            single_pair_item['match_id_1'] = pre_info['match_id']
                            single_pair_item['match_1_home_name'] = pre_info['home_name']
                            single_pair_item['match_1_away_name'] = pre_info['away_name']
                            single_pair_item['match_1_match_time'] = pre_info['match_time']
                            single_pair_item['match_1_home_odd'] = pre_info['home_odd']
                            single_pair_item['match_1_draw_odd'] = pre_info['draw_odd']
                            single_pair_item['match_1_away_odd'] = pre_info['away_odd']
                            single_pair_item['match_id_2'] = match_id
                            single_pair_item['match_2_home_name'] = home_name
                            single_pair_item['match_2_away_name'] = away_name
                            single_pair_item['match_2_match_time'] = match_time
                            single_pair_item['match_2_home_odd'] = home_odd
                            single_pair_item['match_2_draw_odd'] = draw_odd
                            single_pair_item['match_2_away_odd'] = away_odd
                            yield single_pair_item

                    total_arr[league_name].append(current_info)
                else:
                    total_arr[league_name] = [current_info]

        except Exception as err:
            print('%s\n%s' % (err, traceback.format_exc()))
            r = redis.Redis(host='localhost', port=6381, db=0)
            return_url = response.url.split('url=')[1]
            r.lpush('qiutan_crossodds:start_urls', return_url)
            print('重新推入队列！！！%s' % return_url)
            return False
            # pdb.set_trace()
