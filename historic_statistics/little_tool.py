import pdb, traceback
from pymongo import MongoClient
import os
import time


try:
    mongo_client = MongoClient(host='localhost', port=27019)
    db_name = 'cross_odds'
    db = mongo_client[db_name]  # 获得数据库的句柄
    col_name = 'historic_statistics'
    coll = db[col_name]  # 获得collection的句柄

    for item in coll.find({}):
        match_id = item['match_id']
        home_goal = item['home_goal']
        away_goal = item['away_goal']
        if home_goal > away_goal:
            match_result = 3
        elif home_goal == away_goal:
            match_result = 1
        else:
            match_result = 0
        updateItem = dict(match_result = match_result)
        coll.update({"match_id": match_id}, {'$set': updateItem})

except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))
finally:
    mongo_client.close()
