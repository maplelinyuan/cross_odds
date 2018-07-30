# -*- coding:utf-8 -*-
from selenium import webdriver
# from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image, ImageEnhance
import pytesseract
import pdb, traceback
from pymongo import MongoClient
import os
import time
import redis
import json


def get_auth_code(driver, codeEelement):
    '''获取验证码'''
    driver.save_screenshot('login/login.png')  # 截取登录页面
    imgSize = codeEelement.size  # 获取验证码图片的大小
    imgLocation = codeEelement.location  # 获取验证码元素坐标
    rangle = (int(imgLocation['x']), int(imgLocation['y']), int(imgLocation['x'] + imgSize['width']),
              int(imgLocation['y'] + imgSize['height']))  # 计算验证码整体坐标
    login = Image.open("login/login.png")
    frame4 = login.crop(rangle)  # 截取验证码图片
    frame4.save('login/authcode.png')
    authcodeImg = Image.open('login/authcode.png')
    authCodeText = pytesseract.image_to_string(authcodeImg).strip()
    return authCodeText


# 需要修改的url链接
give_me_url = 'http://www.okooo.com/soccer/league/182/schedule/13223/1/'

try:
    mongo_client = MongoClient(host='localhost', port=27019)
    db_name = 'cross_odds'
    db = mongo_client[db_name]  # 获得数据库的句柄
    col_name = 'historic_statistics'
    coll = db[col_name]  # 获得collection的句柄

    service_args = []
    service_args.append('--load-images=no')
    service_args.append('--dick-cache=yes')
    service_args.append('--ignore-ssl-errors=true')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=dcap, service_args=service_args)
    driver.implicitly_wait(20)
    driver.set_page_load_timeout(30)
    driver.get(give_me_url)

    # 删除第一次建立连接时的cookie
    # driver.delete_all_cookies()
    # 读取登录时存储到本地的cookie
    with open('cookies.json', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        driver.add_cookie({
            'domain': 'http://www.okooo.com',  # 此处xxx.com前，需要带点
            'name': cookie['name'],
            'value': cookie['value'],
            'path': '/',
            'expires': None
        })

    league_name = driver.find_elements_by_xpath('//div[@class="LotteryListTitle"]')[0].text  # 联赛名称
    season = driver.find_elements_by_xpath('//div[@class="LotteryListTitle"]')[1].text.split(' ')[1].split('特征')[0]  # 赛季

    end_find_count = 3  # 小于1就提前结束
    first_click = True
    match_day_total = len(driver.find_elements_by_xpath('//td[@class="linkblock"]')) + 1
    for match_day_index in range(0, match_day_total):
        if end_find_count < 1:
            break
        if not first_click:
            match_day_index -= 1
        first_click = False
        windows = driver.window_handles
        driver.switch_to.window(windows[0])
        # print(elem.text)
        driver.find_elements_by_xpath('//td[@class="linkblock"]')[match_day_index].click()
        for single_match in driver.find_elements_by_xpath('//table[@id="team_fight_table"]/tbody/tr[@align="center"]'):
            if single_match.get_attribute('class') == 'LotteryListTitle' or len(single_match.find_elements_by_xpath('td')[3].find_elements_by_xpath('a')) == 0:
                continue
            match_id = single_match.get_attribute('matchid')
            lunci = int(single_match.find_elements_by_xpath('td')[1].text)
            home_name = single_match.find_elements_by_xpath('td')[2].text
            away_name = single_match.find_elements_by_xpath('td')[4].text
            score = single_match.find_elements_by_xpath('td')[3].find_elements_by_xpath('a')[0].find_elements_by_xpath('strong')[0].text
            home_goal = int(score.split('-')[0])
            away_goal = int(score.split('-')[1])
            if home_goal > away_goal:
                match_result = 3
            elif home_goal == away_goal:
                match_result = 1
            else:
                match_result = 0
            single_match.find_elements_by_xpath('td')[-1].find_elements_by_xpath('a')[1].click()
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            driver.find_elements_by_xpath('//div[@id="qnav"]/div')[0].find_elements_by_xpath('a')[0].find_elements_by_xpath('p')[0].click()

            time.sleep(3)
            login_window = driver.find_elements_by_xpath('//div[@id="login_bg"]')[0]
            if login_window.is_displayed():
                print('需要登录！')
                # 方案1，识别验证码，成功率较低
                # user_id_input = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[0].find_elements_by_xpath('input[@id="login_name"]')[0]
                # password_input = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[1].find_elements_by_xpath('input[@id="login_pwd"]')[0]
                # auth_input = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[2].find_elements_by_xpath('dl')[0].find_elements_by_xpath('dd')[0].find_elements_by_xpath('input[@id="AuthCode"]')[0]
                # authcode_img = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[2].find_elements_by_xpath('dl')[0].find_elements_by_xpath('dd')[1].find_elements_by_xpath('p')[0].find_elements_by_xpath('img[@id="randomNoImg"]')[0]
                # login_button = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[5].find_elements_by_xpath('input[@id="LoginSubmit"]')[0]
                # auth_coe = get_auth_code(driver, authcode_img)
                login_window.find_elements_by_xpath('div[@class="mfzc"]')[0].find_elements_by_xpath('p')[
                    1].find_elements_by_xpath('a')[0].click()
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                driver.switch_to.frame("ptlogin_iframe")  # 跳入frame
                driver.find_elements_by_xpath('//span[@id="img_out_1015143338"]')[0].click()
                driver.switch_to.default_content()  # 跳出frame
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                # 获取cookie并通过json模块将dict转化成str
                dictCookies = driver.get_cookies()
                jsonCookies = json.dumps(dictCookies)
                # 登录完成后，将cookie保存到本地文件
                with open('cookies.json', 'w') as f:
                    f.write(jsonCookies)
            else:
                print('已经登录')

            # 获取赔率
            # tr2 竞彩 tr14 威廉 tr82立博 tr27 365 tr43 interwetten tr25 SNAI tr94bwin tr65伟德 tr35易胜博 tr36Eurobet tr37 Expekt tr180 Unibet tr159 博天堂 tr84 澳门 tr250 皇冠 tr220 沙巴 tr280 利记 tr322 金宝博
            try:
                match_time = '20' + WebDriverWait(driver, 15).until(lambda driver: driver.find_elements_by_xpath('//div[@class="qbx_2"]'))[0].find_elements_by_xpath('p')[0].text
                showCZ = driver.find_element_by_id('showCZ')
                if showCZ.is_displayed(): showCZ.click()
                tr2 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr2"))
                tr2_home_odd = float(tr2.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr2_draw_odd = float(tr2.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr2_away_odd = float(tr2.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr14 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr14"))
                tr14_home_odd = float(tr14.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr14_draw_odd = float(tr14.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr14_away_odd = float(tr14.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr82 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr82"))
                tr82_home_odd = float(tr82.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr82_draw_odd = float(tr82.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr82_away_odd = float(tr82.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr27 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr27"))
                tr27_home_odd = float(tr27.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr27_draw_odd = float(tr27.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr27_away_odd = float(tr27.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr43 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr43"))
                tr43_home_odd = float(tr43.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr43_draw_odd = float(tr43.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr43_away_odd = float(tr43.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr25 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr25"))
                tr25_home_odd = float(tr25.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr25_draw_odd = float(tr25.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr25_away_odd = float(tr25.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr94 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr94"))
                tr94_home_odd = float(tr94.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr94_draw_odd = float(tr94.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr94_away_odd = float(tr94.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr65 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr65"))
                tr65_home_odd = float(tr65.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr65_draw_odd = float(tr65.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr65_away_odd = float(tr65.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr35 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr35"))
                tr35_home_odd = float(tr35.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr35_draw_odd = float(tr35.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr35_away_odd = float(tr35.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                # tr36 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr36"))
                # tr36_home_odd = float(tr36.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                # tr36_draw_odd = float(tr36.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                # tr36_away_odd = float(tr36.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr37 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr37"))
                tr37_home_odd = float(tr37.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr37_draw_odd = float(tr37.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr37_away_odd = float(tr37.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr180 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr180"))
                tr180_home_odd = float(tr180.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr180_draw_odd = float(tr180.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr180_away_odd = float(tr180.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr159 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr159"))
                tr159_home_odd = float(tr159.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr159_draw_odd = float(tr159.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr159_away_odd = float(tr159.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr84 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr84"))
                tr84_home_odd = float(tr84.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr84_draw_odd = float(tr84.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr84_away_odd = float(tr84.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                # 向下滚动刷出赔率
                driver.execute_script("window.scrollBy(0, 700)")
                time.sleep(3)
                login_window = driver.find_elements_by_xpath('//div[@id="login_bg"]')[0]
                if login_window.is_displayed():
                    print('需要再次登录！')
                    # 方案1，识别验证码，成功率较低
                    # user_id_input = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[0].find_elements_by_xpath('input[@id="login_name"]')[0]
                    # password_input = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[1].find_elements_by_xpath('input[@id="login_pwd"]')[0]
                    # auth_input = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[2].find_elements_by_xpath('dl')[0].find_elements_by_xpath('dd')[0].find_elements_by_xpath('input[@id="AuthCode"]')[0]
                    # authcode_img = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[2].find_elements_by_xpath('dl')[0].find_elements_by_xpath('dd')[1].find_elements_by_xpath('p')[0].find_elements_by_xpath('img[@id="randomNoImg"]')[0]
                    # login_button = login_window.find_elements_by_xpath('div[@class="loginbox_login"]')[0].find_elements_by_xpath('ul[@id="head_login_info"]')[0].find_elements_by_xpath('li')[5].find_elements_by_xpath('input[@id="LoginSubmit"]')[0]
                    # auth_coe = get_auth_code(driver, authcode_img)
                    login_window.find_elements_by_xpath('div[@class="mfzc"]')[0].find_elements_by_xpath('p')[
                        1].find_elements_by_xpath('a')[0].click()
                    windows = driver.window_handles
                    driver.switch_to.window(windows[-1])
                    driver.switch_to.frame("ptlogin_iframe")  # 跳入frame
                    driver.find_elements_by_xpath('//span[@id="img_out_1015143338"]')[0].click()
                    driver.switch_to.default_content()  # 跳出frame
                    windows = driver.window_handles
                    driver.switch_to.window(windows[-1])
                    # 获取cookie并通过json模块将dict转化成str
                    dictCookies = driver.get_cookies()
                    jsonCookies = json.dumps(dictCookies)
                    # 登录完成后，将cookie保存到本地文件
                    with open('cookies.json', 'w') as f:
                        f.write(jsonCookies)
                    time.sleep(3)
                    driver.execute_script("window.scrollBy(0, 700)")
                    # driver.find_element_by_id('showCZ').click()
                else:
                    print('已经登录')
                tr250 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr250"))
                tr250_home_odd = float(tr250.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr250_draw_odd = float(tr250.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr250_away_odd = float(tr250.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr220 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr220"))
                tr220_home_odd = float(tr220.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr220_draw_odd = float(tr220.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr220_away_odd = float(tr220.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr280 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr280"))
                tr280_home_odd = float(tr280.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr280_draw_odd = float(tr280.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr280_away_odd = float(tr280.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)
                tr322 = WebDriverWait(driver, 15).until(lambda driver: driver.find_element_by_id("tr322"))
                tr322_home_odd = float(tr322.find_elements_by_xpath('td')[2].find_elements_by_xpath('span')[0].text)
                tr322_draw_odd = float(tr322.find_elements_by_xpath('td')[3].find_elements_by_xpath('span')[0].text)
                tr322_away_odd = float(tr322.find_elements_by_xpath('td')[4].find_elements_by_xpath('span')[0].text)

                insertItem = dict(
                    match_id=match_id,
                    season=season,
                    lunci=lunci,
                    league_name=league_name,
                    match_time=match_time,
                    home_name=home_name,
                    away_name=away_name,
                    home_goal=home_goal,
                    away_goal=away_goal,
                    match_result=match_result,
                    jingcai_home=tr2_home_odd,
                    jingcai_draw=tr2_draw_odd,
                    jingcai_away=tr2_away_odd,
                    weilian_home=tr14_home_odd,
                    weilian_draw=tr14_draw_odd,
                    weilian_away=tr14_away_odd,
                    libo_home=tr82_home_odd,
                    libo_draw=tr82_draw_odd,
                    libo_away=tr82_away_odd,
                    bet365_home=tr27_home_odd,
                    bet365_draw=tr27_draw_odd,
                    bet365_away=tr27_away_odd,
                    inter_home=tr43_home_odd,
                    inter_draw=tr43_draw_odd,
                    inter_away=tr43_away_odd,
                    snai_home=tr25_home_odd,
                    snai_draw=tr25_draw_odd,
                    snai_away=tr25_away_odd,
                    bwin_home=tr94_home_odd,
                    bwin_draw=tr94_draw_odd,
                    bwin_away=tr94_away_odd,
                    weide_home=tr65_home_odd,
                    weide_draw=tr65_draw_odd,
                    weide_away=tr65_away_odd,
                    yishengbo_home=tr35_home_odd,
                    yishengbo_draw=tr35_draw_odd,
                    yishengbo_away=tr35_away_odd,
                    # eurobet_home=tr36_home_odd,
                    # eurobet_draw=tr36_draw_odd,
                    # eurobet_away=tr36_away_odd,
                    expekt_home=tr37_home_odd,
                    expekt_draw=tr37_draw_odd,
                    expekt_away=tr37_away_odd,
                    unibet_home=tr180_home_odd,
                    unibet_draw=tr180_draw_odd,
                    unibet_away=tr180_away_odd,
                    botiantang_home=tr159_home_odd,
                    botiantang_draw=tr159_draw_odd,
                    botiantang_away=tr159_away_odd,
                    aomen_home=tr84_home_odd,
                    aomen_draw=tr84_draw_odd,
                    aomen_away=tr84_away_odd,
                    crown_home=tr250_home_odd,
                    crown_draw=tr250_draw_odd,
                    crown_away=tr250_away_odd,
                    shaba_home=tr220_home_odd,
                    shaba_draw=tr220_draw_odd,
                    shaba_away=tr220_away_odd,
                    liji_home=tr280_home_odd,
                    liji_draw=tr280_draw_odd,
                    liji_away=tr280_away_odd,
                    jinbaobo_home=tr322_home_odd,
                    jinbaobo_draw=tr322_draw_odd,
                    jinbaobo_away=tr322_away_odd,

                )
                if coll.find({'match_id': match_id}).count() == 0:
                    coll.insert(insertItem)
            except Exception as err:
                print('%s\n%s' % (err, traceback.format_exc()))
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            driver.close()
            driver.switch_to.window(windows[0])

    # 关闭窗口
    driver.quit()

except Exception as err:
    print('%s\n%s' % (err, traceback.format_exc()))
finally:
    mongo_client.close()



