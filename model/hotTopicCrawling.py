#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:  Xinyi Hu
# contact: samaritanhu@gmail.com

import requests
import json

headers = {
    'charset': "utf-8",
    'Accept-Encoding': "gzip",
    'referer': "https://servicewechat.com/wx90ae92bbd13ec629/11/page-frame.html",
    'content-type': "application/x-www-form-urlencoded",
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/7.0.3.1400(0x2700033B) Process/appbrand0 NetType/WIFI Language/zh_CN",
    'Host': "www.eecso.com",
    'Connection': "keep-alive",
    'cache-control': "no-cache",
    'Origin': 'https://www.weibotop.cn',
}


def fetch_weibo_topic():
    with open('微博热搜.csv', 'w', encoding='gbk') as f:
        f.write('时间,排名,热搜内容,最后时间,上榜时间\n')

    timeid = 65385-24*30*20+3+11*30
    dateUrl = "https://www.eecso.com/test/weibo/apis/getlatest.php?timeid={}"
    contentUrl = "https://www.eecso.com/test/weibo/apis/currentitems.php?timeid={}"
    n = 1
    interval = 30 #改为1则是爬所有数据（该网站2分钟记录一次） 24*30 = 720
    for _ in range(24*30):
        dateResponse = requests.request("GET", dateUrl.format(timeid), headers=headers,verify=False)
        contentResponse = requests.request("GET", contentUrl.format(timeid), headers=headers,verify=False)
        timeid = 65385-24*30*20+3+11*30-interval*n #77594为2020/2/10 12:00的timeid，720为一天timeid的间隔
        print(timeid)
        n += 1
        dateJson = json.loads(dateResponse.text)
        json_obj = json.loads(contentResponse.text)

        for index,item in enumerate(json_obj):
            date = dateJson[1]
            rank = str(index+1)
            hotTopic = item[0]
            onTime = item[1]
            lastTime = item[2]
            save_res = date+","+rank+","+hotTopic+','+onTime+','+lastTime+'\n'
            with open('微博热搜.csv','a',encoding='gbk',errors='ignore') as f:
                f.write(save_res)


if __name__ == '__main__':
    fetch_weibo_topic()