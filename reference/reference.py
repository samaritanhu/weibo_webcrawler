#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:  Xinyi Hu
# contact: samaritanhu@gmail.com

import requests
import time
import json
import random
headers = {
    'charset': "utf-8",
    'Accept-Encoding': "gzip",
    'referer': "https://servicewechat.com/wx90ae92bbd13ec629/11/page-frame.html",
    'content-type': "application/x-www-form-urlencoded",
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/7.0.3.1400(0x2700033B) Process/appbrand0 NetType/WIFI Language/zh_CN",
    'Host': "www.enlightent.cn",
    'Connection': "keep-alive",
    'cache-control': "no-cache",
}

#获取每一天的日期！！！!!!
def get_date():
    date_list = []
    year_list = [2020,2019,2018,2017]
    month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    fun = lambda year, month: list(range(1, 1+time.localtime(time.mktime((year,month+1,1,0,0,0,0,0,0)) - 86400).tm_mday))

    for year in year_list:
        for month in month_list:
            day_list = fun(year, month)
            for day in day_list:
                save_res = str(year)+'%2f'+str(month)+'%2f'+str(day)
                date_list.append(save_res)

    return date_list


def start():
    with open('微博热搜.csv', 'w', encoding='gbk') as f:
        f.write('日期,排名,时间名称,搜索量,当时最高排名\n')

    date_list = get_date()

    url = "https://www.enlightent.cn/research/top/getWeiboHotSearchDayAggs.do"

    for date in date_list:
        payload = "date={date}&type=realTimeHotSearchList"
        data = payload.format(date=date)
        response = requests.request("POST", url, data=data, headers=headers,verify=False)
        print(response.text)
        json_obj = json.loads(response.text)

        num = 1
        for item in json_obj:
            save_date = date.replace('%2f','-')
            save_num = str(num)
            num+=1
            name = item['keyword'].replace(',','，')
            searchCount = str(item['searchCount'])
            rank = str(item['rank'])

            save_res = save_date+','+save_num+','+name+','+searchCount+','+rank+'\n'
            print(save_res)
            with open('微博热搜.csv','a',encoding='gbk',errors='ignore') as f:
                f.write(save_res)


if __name__ == '__main__':
    print(get_date())