import pdb, traceback
from pymongo import MongoClient
import os
import time

try:
    mongo_client = MongoClient(host='localhost', port=27019)
    db_name = 'cross_odds'
    db = mongo_client[db_name]  # 获得数据库的句柄
    col_name = 'historic_statistics_result'
    coll = db[col_name]  # 获得collection的句柄
    company_arr = ['jingcai', 'weilian', 'libo', 'bet365', 'inter', 'snai', 'bwin', 'weide', 'yishengbo', 'expekt', 'unibet', 'botiantang', 'aomen', 'crown', 'shaba', 'liji', 'jinbaobo']
    my_company_arr = ['weilian', 'libo', 'snai', 'bwin', 'yishengbo', 'botiantang', 'crown']
    for company in company_arr:
        if company in my_company_arr:
            total = 0
            result_equal_count = 0
            for item in coll.find({}):
                equal_company_name = item['equal_company_name']
                match_1_home_odd = item['match_1_home_odd']
                match_1_draw_odd = item['match_1_draw_odd']
                match_1_away_odd = item['match_1_away_odd']
                match_2_home_odd = item['match_2_home_odd']
                match_2_draw_odd = item['match_2_draw_odd']
                match_2_away_odd = item['match_2_away_odd']
                match_time_1 = item['match_time_1']
                match_time_2 = item['match_time_2']
                timeArray_1 = time.strptime(match_time_1, "%Y-%m-%d %H:%M")
                timeArray_2 = time.strptime(match_time_2, "%Y-%m-%d %H:%M")
                # 转换成时间戳
                timestamp_1 = time.mktime(timeArray_1)
                timestamp_2 = time.mktime(timeArray_2)
                limit_odd = 1.85

                # 策略1 买平局
                if equal_company_name == company:
                    if match_1_home_odd <= limit_odd or match_1_away_odd <= limit_odd:
                        result_1 = item['match_result_1']
                        result_2 = item['match_result_2']
                        total += 2
                        if result_1 == 1:
                            result_equal_count += match_1_draw_odd
                        if result_2 == 1:
                            result_equal_count += match_2_draw_odd
                # 策略2 买下盘
                # if equal_company_name == company:
                #     if match_1_home_odd <= limit_odd or match_1_away_odd <= limit_odd:
                #         result_1 = item['match_result_1']
                #         result_2 = item['match_result_2']
                #         total += 2
                #         if (match_1_home_odd < match_1_away_odd) and (result_1 == 1 or result_1 == 0):
                #             result_equal_count += (match_1_draw_odd+match_1_away_odd)/4
                #         if (match_1_home_odd > match_1_away_odd) and (result_1 == 3 or result_1 == 1):
                #             result_equal_count += (match_1_draw_odd+match_1_home_odd)/4
                #         if (match_2_home_odd < match_2_away_odd) and (result_2 == 1 or result_2 == 0):
                #             result_equal_count += (match_2_draw_odd+match_2_away_odd)/4
                #         if (match_2_home_odd > match_2_away_odd) and (result_2 == 3 or result_2 == 1):
                #             result_equal_count += (match_2_draw_odd+match_2_home_odd)/4
                # 策略3 第一场低赔后买下盘
                # if equal_company_name == company:
                #     if timestamp_1 + 105*60 < timestamp_2:
                #         if match_1_home_odd <= limit_odd or match_1_away_odd <= limit_odd:
                #             result_1 = item['match_result_1']
                #             result_2 = item['match_result_2']
                #             # if ((match_1_home_odd <= limit_odd and result_1 == 3) or (match_1_away_odd <= limit_odd and result_1 == 0)) and ((match_2_home_odd <= limit_odd and result_2 == 3) or (match_2_away_odd <= limit_odd and result_2 == 0)):
                #             if (match_1_home_odd <= limit_odd and result_1 == 3) or (match_1_away_odd <= limit_odd and result_1 == 0):
                #                 total += 1
                #                 # 如果第一场低赔打出，第二场买下盘
                #                 if (match_2_home_odd <= limit_odd and result_2 == 3) or (match_2_away_odd <= limit_odd and result_2 == 0):
                #                     pass
                #                 else:
                #                     if match_2_away_odd > match_2_home_odd:
                #                         result_equal_count += (match_2_away_odd + match_2_draw_odd) / 4
                #                     else:
                #                         result_equal_count += (match_2_home_odd + match_2_draw_odd) / 4

            print('公司：%s, 总数：%s, 利润： %s' % (company, total, result_equal_count - total))

except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))
finally:
    mongo_client.close()