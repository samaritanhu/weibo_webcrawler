#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:  Xinyi Hu
# contact: samaritanhu@gmail.com
# date: 7/17/19
from lxml import html
import xml
import requests
from selenium import webdriver
import xlwt  # 导入excel库
import time  # 导入延时库
import calendar

# 目标爬取的网址 和 Chromedriver的配置
url = "http://www.enlightent.cn/analytics/top/rank_tv"
wbk = xlwt.Workbook()
driver = webdriver.Chrome(executable_path=r'C:\Users\huxinyi_sx\anaconda3\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe')
driver.get(url)


# 表格初始化
sheet = wbk.add_sheet('2019年')
sheet.write(0,0,'id')
sheet.write(0,1,'日期')
for i in range(10):
    sheet.write(0, 4 * i + 2, '序号')
    sheet.write(0, 4 * i + 3, '片名')
    sheet.write(0, 4 * i + 4, '正片有效播放市场占有率')
    sheet.write(0, 4 * i + 5, '日前台点击量')

# 登录微信
time.sleep(15)
driver.get(url)

id = 1

for l in range(7):
    start_date, month_length = calendar.monthrange(2019, l + 1)
    if start_date == 0:
        start_date = 7
    if l == 6:
        month_length = 17

    # 选择日榜
    time.sleep(5)
    driver.find_elements_by_id("rank-date-btn")[0].click()
    # 选择换年份
    time.sleep(1)
    driver.find_element_by_class_name("datepicker-switch").click()
    # 选择目标月份
    time.sleep(1)
    # driver.find_element_by_class_name("month").click()
    month_url = "/html/body/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div/div/div[2]/table/tbody/tr/td/span[%s]" % (l+1)
    driver.find_element_by_xpath(month_url).click()
    # 选择目标日期
    time.sleep(1)
    # day = driver.find_element_by_class_name("day").click()
    xpath = "/html/body/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div/div/div/table/tbody/tr[%d]/td[%d]" \
            % ((start_date) // 7 + 1, (start_date) % 7 + 1)
    driver.find_element_by_xpath(xpath).click()

    #driver.find_element_by_xpath(
    #    "/html/body/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div/div/div/table/tbody/tr[1]/td[2]").click()
    # 点击确定
    time.sleep(1)
    driver.find_element_by_id("choose-rank").click()
    time.sleep(1)

    for k in range(month_length):
        # 选择日榜
        time.sleep(1)
        driver.find_elements_by_id("rank-date-btn")[0].click()
        # 选择日期
        time.sleep(1)
        xpath = "/html/body/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div/div/div/table/tbody/tr[%d]/td[%d]" \
                % ((k + start_date) // 7 + 1, (k + start_date) % 7 + 1)
        driver.find_element_by_xpath(xpath).click()
        # 点击确定
        time.sleep(1)
        driver.find_element_by_id("choose-rank").click()
        time.sleep(2)

        string_all = driver.page_source  # 将所有数据扒取，并以字符串形式存放
        string_choose = string_all[
                        string_all.find('<tr data-index="0">'):string_all.find('<td class="rank-average m-change">')]  # 初步处理数据，锁定热搜范围，type:str
        string_list = string_choose.split('<a class="rank-more-btn" href="JavaScript:;"')

        album = []
        percentage = []
        click = []
        for j in range(0,11):
            album_separately = string_list[j][string_list[j].find('data-name='):string_list[j].find('data-channeltype="tv"')]
            if j != 0:
                album.append(album_separately.replace('data-name=','').replace('"',''))
                print(album_separately.replace('data-name=','').replace('"',''))
            percentage_separately = string_list[j][string_list[j].find('<td class="sort rank-playTimesPredicted active" style=""><span>'):string_list[j].find('</span></td><td class="rank-playTimes" style="">')]
            print(percentage_separately.replace('<td class="sort rank-playTimesPredicted active" style=""><span>',''))
            percentage.append(percentage_separately.replace('<td class="sort rank-playTimesPredicted active" style=""><span>',''))
            click_separately = string_list[j][string_list[j].find('</td><td class="rank-playTimes" style=""><span>'):string_list[j].find('</span><span class="star-playtimes">')]
            if len(click_separately) >= 10:
                click_separately = string_list[j][
                                    string_list[j].find('</td><td class="rank-playTimes" style=""><span>'):string_list[j].find(
                                        '</span></td><td class="rank-average m-change" style="">')]
            print(click_separately.replace('</td><td class="rank-playTimes" style=""><span>','').replace('</span><span class="star-playtimes">',''))
            click.append(click_separately.replace('</td><td class="rank-playTimes" style=""><span>','').replace('</span><span class="star-playtimes">',''))

        date = '2019年%d月%d日' % ((l + 1), (k + 1))
        print('现在正在读入...', date)
        sheet.write(id, 0, id)
        sheet.write(id, 1, date)
        for i in range(10):
            sheet.write(id, 4 * i + 2, i + 1)
            sheet.write(id, 4 * i + 3, album[i])
            sheet.write(id, 4 * i + 4, percentage[i])
            sheet.write(id, 4 * i + 5, click[i])
        id += 1

wbk.save('D:\\tvshow_2019.xls')


driver.quit()  # 关闭后台浏览器防止内存超载
print('success!')
