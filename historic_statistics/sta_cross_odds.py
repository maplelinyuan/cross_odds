import pdb, traceback
from pymongo import MongoClient
import os
import time

season_arr = ['17/18', '2017']
league_arr = ['英超', '西甲', '德甲', '法甲', '意甲', '瑞典超', '葡超', '英冠', '西乙', '德乙', '法乙', '意乙']

try:
    mongo_client = MongoClient(host='localhost', port=27019)
    db_name = 'cross_odds'
    db = mongo_client[db_name]  # 获得数据库的句柄
    col_name = 'historic_statistics'
    coll = db[col_name]  # 获得collection的句柄

    for season in season_arr:
        for league in league_arr:
            for i in range(1, 49):
                # 每轮开始
                matchid_arr = []
                jingcai_arr = []
                weilian_arr = []
                libo_arr = []
                bet365_arr = []
                inter_arr = []
                snai_arr = []
                bwin_arr = []
                weide_arr = []
                yishengbo_arr = []
                expekt_arr = []
                unibet_arr = []
                botiantang_arr = []
                aomen_arr = []
                crown_arr = []
                shaba_arr = []
                liji_arr = []
                jinbaobo_arr = []
                for item in coll.find({'season': season, 'league_name': league, 'lunci': i}):
                    matchid_arr.append(item['match_id'])
                    jingcai_odd = [item['jingcai_home'], item['jingcai_draw'], item['jingcai_away']]
                    weilian_odd = [item['weilian_home'], item['weilian_draw'], item['weilian_away']]
                    libo_odd = [item['libo_home'], item['libo_draw'], item['libo_away']]
                    bet365_odd = [item['bet365_home'], item['bet365_draw'], item['bet365_away']]
                    inter_odd = [item['inter_home'], item['inter_draw'], item['inter_away']]
                    snai_odd = [item['snai_home'], item['snai_draw'], item['snai_away']]
                    bwin_odd = [item['bwin_home'], item['bwin_draw'], item['bwin_away']]
                    weide_odd = [item['weide_home'], item['weide_draw'], item['weide_away']]
                    yishengbo_odd = [item['yishengbo_home'], item['yishengbo_draw'], item['yishengbo_away']]
                    expekt_odd = [item['expekt_home'], item['expekt_draw'], item['expekt_away']]
                    unibet_odd = [item['unibet_home'], item['unibet_draw'], item['unibet_away']]
                    botiantang_odd = [item['botiantang_home'], item['botiantang_draw'], item['botiantang_away']]
                    aomen_odd = [item['aomen_home'], item['aomen_draw'], item['aomen_away']]
                    crown_odd = [item['crown_home'], item['crown_draw'], item['crown_away']]
                    shaba_odd = [item['shaba_home'], item['shaba_draw'], item['shaba_away']]
                    liji_odd = [item['liji_home'], item['liji_draw'], item['liji_away']]
                    jinbaobo_odd = [item['jinbaobo_home'], item['jinbaobo_draw'], item['jinbaobo_away']]
                    jingcai_arr.append(jingcai_odd)
                    weilian_arr.append(weilian_odd)
                    libo_arr.append(libo_odd)
                    bet365_arr.append(bet365_odd)
                    inter_arr.append(inter_odd)
                    snai_arr.append(snai_odd)
                    bwin_arr.append(bwin_odd)
                    weide_arr.append(weide_odd)
                    yishengbo_arr.append(yishengbo_odd)
                    expekt_arr.append(expekt_odd)
                    unibet_arr.append(unibet_odd)
                    botiantang_arr.append(botiantang_odd)
                    aomen_arr.append(aomen_odd)
                    crown_arr.append(crown_odd)
                    shaba_arr.append(shaba_odd)
                    liji_arr.append(liji_odd)
                    jinbaobo_arr.append(jinbaobo_odd)
                # 每轮结束
                arr_len = len(matchid_arr)
                equal_match_id_arr = []     # 相等赔率的ID对列表[[1,5],[2,3]]
                equal_match_id_map_arr = []     # 两个ID映射成的唯一数字，用来确定是否存在了match_id
                equal_match_company_arr = []        # 相等赔率的公司
                for j in range(0, arr_len):
                    for k in range(j+1, arr_len):
                        if (jingcai_arr[j][0] == jingcai_arr[k][0] and jingcai_arr[j][1] == jingcai_arr[k][1] and jingcai_arr[j][2] == jingcai_arr[k][2]) or (jingcai_arr[j][0] == jingcai_arr[k][2] and jingcai_arr[j][1] == jingcai_arr[k][1] and jingcai_arr[j][2] == jingcai_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('jingcai')
                            continue
                        if (weilian_arr[j][0] == weilian_arr[k][0] and weilian_arr[j][1] == weilian_arr[k][1] and weilian_arr[j][2] == weilian_arr[k][2]) or (weilian_arr[j][0] == weilian_arr[k][2] and weilian_arr[j][1] == weilian_arr[k][1] and weilian_arr[j][2] == weilian_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('weilian')
                            continue
                        if (libo_arr[j][0] == libo_arr[k][0] and libo_arr[j][1] == libo_arr[k][1] and libo_arr[j][2] == libo_arr[k][2]) or (libo_arr[j][0] == libo_arr[k][2] and libo_arr[j][1] == libo_arr[k][1] and libo_arr[j][2] == libo_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('libo')
                            continue
                        if (bet365_arr[j][0] == bet365_arr[k][0] and bet365_arr[j][1] == bet365_arr[k][1] and bet365_arr[j][2] == bet365_arr[k][2]) or (bet365_arr[j][0] == bet365_arr[k][2] and bet365_arr[j][1] == bet365_arr[k][1] and bet365_arr[j][2] == bet365_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('bet365')
                            continue
                        if (inter_arr[j][0] == inter_arr[k][0] and inter_arr[j][1] == inter_arr[k][1] and inter_arr[j][2] == inter_arr[k][2]) or (inter_arr[j][0] == inter_arr[k][2] and inter_arr[j][1] == inter_arr[k][1] and inter_arr[j][2] == inter_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('inter')
                            continue
                        if (snai_arr[j][0] == snai_arr[k][0] and snai_arr[j][1] == snai_arr[k][1] and snai_arr[j][2] == snai_arr[k][2]) or (snai_arr[j][0] == snai_arr[k][2] and snai_arr[j][1] == snai_arr[k][1] and snai_arr[j][2] == snai_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('snai')
                            continue
                        if (bwin_arr[j][0] == bwin_arr[k][0] and bwin_arr[j][1] == bwin_arr[k][1] and bwin_arr[j][2] == bwin_arr[k][2]) or (bwin_arr[j][0] == bwin_arr[k][2] and bwin_arr[j][1] == bwin_arr[k][1] and bwin_arr[j][2] == bwin_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('bwin')
                            continue
                        if (weide_arr[j][0] == weide_arr[k][0] and weide_arr[j][1] == weide_arr[k][1] and weide_arr[j][2] == weide_arr[k][2]) or (weide_arr[j][0] == weide_arr[k][2] and weide_arr[j][1] == weide_arr[k][1] and weide_arr[j][2] == weide_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('weide')
                            continue
                        if (yishengbo_arr[j][0] == yishengbo_arr[k][0] and yishengbo_arr[j][1] == yishengbo_arr[k][1] and yishengbo_arr[j][2] == yishengbo_arr[k][2]) or (yishengbo_arr[j][0] == yishengbo_arr[k][2] and yishengbo_arr[j][1] == yishengbo_arr[k][1] and yishengbo_arr[j][2] == yishengbo_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('yishengbo')
                            continue
                        if (expekt_arr[j][0] == expekt_arr[k][0] and expekt_arr[j][1] == expekt_arr[k][1] and expekt_arr[j][2] == expekt_arr[k][2]) or (expekt_arr[j][0] == expekt_arr[k][2] and expekt_arr[j][1] == expekt_arr[k][1] and expekt_arr[j][2] == expekt_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('expekt')
                            continue
                        if (unibet_arr[j][0] == unibet_arr[k][0] and unibet_arr[j][1] == unibet_arr[k][1] and unibet_arr[j][2] == unibet_arr[k][2]) or (unibet_arr[j][0] == unibet_arr[k][2] and unibet_arr[j][1] == unibet_arr[k][1] and unibet_arr[j][2] == unibet_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('unibet')
                            continue
                        if (botiantang_arr[j][0] == botiantang_arr[k][0] and botiantang_arr[j][1] == botiantang_arr[k][1] and botiantang_arr[j][2] == botiantang_arr[k][2]) or (botiantang_arr[j][0] == botiantang_arr[k][2] and botiantang_arr[j][1] == botiantang_arr[k][1] and botiantang_arr[j][2] == botiantang_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('botiantang')
                            continue
                        if (aomen_arr[j][0] == aomen_arr[k][0] and aomen_arr[j][1] == aomen_arr[k][1] and aomen_arr[j][2] == aomen_arr[k][2]) or (aomen_arr[j][0] == aomen_arr[k][2] and aomen_arr[j][1] == aomen_arr[k][1] and aomen_arr[j][2] == aomen_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('aomen')
                            continue
                        if (crown_arr[j][0] == crown_arr[k][0] and crown_arr[j][1] == crown_arr[k][1] and crown_arr[j][2] == crown_arr[k][2]) or (crown_arr[j][0] == crown_arr[k][2] and crown_arr[j][1] == crown_arr[k][1] and crown_arr[j][2] == crown_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('crown')
                            continue
                        if (shaba_arr[j][0] == shaba_arr[k][0] and shaba_arr[j][1] == shaba_arr[k][1] and shaba_arr[j][2] == shaba_arr[k][2]) or (shaba_arr[j][0] == shaba_arr[k][2] and shaba_arr[j][1] == shaba_arr[k][1] and shaba_arr[j][2] == shaba_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('shaba')
                            continue
                        if (liji_arr[j][0] == liji_arr[k][0] and liji_arr[j][1] == liji_arr[k][1] and liji_arr[j][2] == liji_arr[k][2]) or (liji_arr[j][0] == liji_arr[k][2] and liji_arr[j][1] == liji_arr[k][1] and liji_arr[j][2] == liji_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('liji')
                            continue
                        if (jinbaobo_arr[j][0] == jinbaobo_arr[k][0] and jinbaobo_arr[j][1] == jinbaobo_arr[k][1] and jinbaobo_arr[j][2] == jinbaobo_arr[k][2]) or (jinbaobo_arr[j][0] == jinbaobo_arr[k][2] and jinbaobo_arr[j][1] == jinbaobo_arr[k][1] and jinbaobo_arr[j][2] == jinbaobo_arr[k][0]):
                            match_2_t_1_map = int(matchid_arr[j]) * int(matchid_arr[k])
                            if not match_2_t_1_map in equal_match_id_map_arr:
                                equal_match_id_map_arr.append(match_2_t_1_map)
                                equal_match_id_arr.append([matchid_arr[j], matchid_arr[k]])
                                equal_match_company_arr.append('jinbaobo')
                            continue

                # 开始输出
                sub_col_name = 'historic_statistics_result'
                sub_coll = db[sub_col_name]  # 获得collection的句柄
                inc = 0
                for equal_match_pair in equal_match_id_arr:
                    match_id_1 = equal_match_pair[0]
                    match_id_2 = equal_match_pair[1]
                    equal_company_name = equal_match_company_arr[inc]
                    match_time_1 = coll.find_one({'match_id': match_id_1})['match_time']
                    match_time_2 = coll.find_one({'match_id': match_id_2})['match_time']
                    match_1_home_odd = coll.find_one({'match_id': match_id_1})[equal_company_name+'_home']
                    match_1_draw_odd = coll.find_one({'match_id': match_id_1})[equal_company_name+'_draw']
                    match_1_away_odd = coll.find_one({'match_id': match_id_1})[equal_company_name+'_away']
                    match_2_home_odd = coll.find_one({'match_id': match_id_2})[equal_company_name + '_home']
                    match_2_draw_odd = coll.find_one({'match_id': match_id_2})[equal_company_name + '_draw']
                    match_2_away_odd = coll.find_one({'match_id': match_id_2})[equal_company_name + '_away']
                    match_result_1 = coll.find_one({'match_id': match_id_1})['match_result']
                    match_result_2 = coll.find_one({'match_id': match_id_2})['match_result']
                    insertItem = dict(equal_company_name=equal_company_name, match_id_1=match_id_1, match_time_1=match_time_1, match_id_2=match_id_2, match_time_2=match_time_2, match_result_1=match_result_1, match_result_2 = match_result_2,
                                      match_1_home_odd=match_1_home_odd, match_1_draw_odd=match_1_draw_odd, match_1_away_odd=match_1_away_odd,
                                      match_2_home_odd=match_2_home_odd, match_2_draw_odd=match_2_draw_odd, match_2_away_odd=match_2_away_odd)
                    if sub_coll.find({'match_id_1': match_id_1}).count() == 0:
                        sub_coll.insert(insertItem)
                    print('轮次：%s, 比赛：%s和%s, 公司：%s' % (i, match_id_1, match_id_2, equal_company_name))
                    inc += 1


except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))
finally:
    mongo_client.close()