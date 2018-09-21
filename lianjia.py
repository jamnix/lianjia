#!/usr/bin/python
#-*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import MySQLdb
import json
import time
import random


#全局变量
#set header

table='lianjia_270_310'
conn = MySQLdb.connect(host='localhost', user='root', port=3306, passwd='123', db='lianjia')

host_url="http://sz.lianjia.com/"
global total_page_num
global header
total_page_num = 0
header = {}


#输入
init_page=1
url = "http://sz.lianjia.com/ershoufang/pg%dl2l3bp270ep310/"

def init():
    global header
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.32 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    header['Host'] = "sz.lianjia.com"
    header['Accept-Language'] = "zh-CN,zh;q=0.8,en;q=0.6"
    header['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    #header['Accept-Encoding'] = "gzip,.deflate"
    header['Referer'] = "http://sz.lianjia.com/ershoufang/"
    header['Connection'] = "keep-alive"
    header['Cookie'] = "lianjia_uuid=23ac3353-d618-4d64-8756-6617aa2ac6d2; lianjia_token=2.004bce38283106c4865a6311192a01c38a; Hm_lvt_efa595b768cc9dc7d7f9823368e795f1=1488093925; _UC_agent=1; UM_distinctid=15ab8c51d72209-08142421620818-5b123112-100200-15ab8c51d73332; all-lj=59dc31ee6d382c2bb143f566d268070e; select_city=440300; _ga=GA1.2.1004029969.1485352479; _smt_uid=5888ae1c.3490f4cf; lianjia_ssid=3c0201a4-2b4b-406b-8ced-e61872bce9e2"


def insert_db(url):
    init()
    global total_page_num

    request=urllib2.Request(url, headers=header)
    for retry in range(10):
        try:
            print ">>>>>>>>>>>try calling %s %d time"%(url, retry)
            content=urllib2.urlopen(request, timeout=5).read()
            break;
        except :
            continue
    soup = BeautifulSoup(content, 'html.parser');
    #print soup.title.name

    #total page num
    page_num_class = soup.find('div', class_='page-box house-lst-page-box')
    page_num_json = json.loads(page_num_class["page-data"].encode('utf-8'))
    total_page_num = int(page_num_json["totalPage"])
    print ">>>>>>>>>>>%d"%total_page_num
            

    page = soup.find('ul', class_='sellListContent')
    for house in page.find_all('li'):
        #time.sleep(1)
        init()
        cur = conn.cursor()

        #获取href
        href_class = house.find('div', class_='title')
        href=href_class.a["href"].encode('utf-8')
        #title=item.a.string

        house_request=urllib2.Request(href, headers=header)
        for retry in range(10):
            try:
                print ">>>>>>>>>>>>>>try calling %s %d time"%(href, retry)
                house_content = urllib2.urlopen(house_request, timeout=5).read() 
                break;
            except:
                continue;
        house_soup = BeautifulSoup(house_content, 'html.parser')

        #div:sellDetailHeader
        sellDetailHeader = house_soup.find('div', class_='sellDetailHeader')
        title_class = sellDetailHeader.find('div', class_='title')
        title = title_class.h1.string.encode('utf-8') 
        title_sub = title_class.div.string.encode('utf-8') 

        #div:overview
        overview_class = house_soup.find('div', class_='overview')

        price = overview_class.find('span', class_='total').string.encode('utf-8')
        unit_price = overview_class.find('span', class_='unitPriceValue').contents[0].encode('utf-8')

        room_class = overview_class.find('div', class_='room')
        room_huxing = room_class.find('div', class_='mainInfo').string.encode('utf-8')
        room_loucheng = room_class.find('div', class_='subInfo').string.encode('utf-8')

        type_class = overview_class.find('div', class_='type')
        room_fangxiang = type_class.find('div', class_='mainInfo').string.encode('utf-8')
        room_zhuanxiu = type_class.find('div', class_='subInfo').string.encode('utf-8')

        area = overview_class.find('div', class_='area')
        room_size = area.find('div', class_='mainInfo').string.encode('utf-8')
        room_has_year = area.find('div', class_='subInfo').string.encode('utf-8')

        communityName = overview_class.find('div', class_='communityName')
        xiaoqu_name = communityName.find('a', class_='info').string.encode('utf-8')
        xiaoqu_href = host_url + communityName.find('a', class_='info')['href'].encode('utf-8')

        areaName = overview_class.find('div', class_='areaName')
        area_qu = areaName.find('span', class_='info').contents[0].string.encode('utf-8')
        area_qu_sub = areaName.find('span', class_='info').contents[2].string.encode('utf-8')
        
        #m-content
        m_content_class = house_soup.find('div', class_='m-content')
        introContent_class = m_content_class.find('div', class_='introContent')
        base_class = introContent_class.find('div', class_='base')
        for item in base_class.find('div', class_='content').ul.find_all('li'):
            if item.span.string.encode('utf-8') == "房屋户型":
                   room_huxing = item.contents[1].encode('utf-8')      
            if item.span.string.encode('utf-8') == "梯户比例":
                   room_tihu = item.contents[1].encode('utf-8')       
            if item.span.string.encode('utf-8') == "配备电梯":
                   room_dianti = item.contents[1].encode('utf-8')       
            if item.span.string.encode('utf-8') == "产权年限":
                   room_chanquan = item.contents[1].encode('utf-8')       

        transaction_class = introContent_class.find('div', class_='transaction')
        for item in transaction_class.find('div', class_='content').ul.find_all('li'):
            if item.span.string.encode('utf-8') == "挂牌时间":
                   room_now_buy = item.contents[1].encode('utf-8')       
            if item.span.string.encode('utf-8') == "交易权属":
                   room_shanping = item.contents[1].encode('utf-8')       
            if item.span.string.encode('utf-8') == "上次交易":
                   room_last_buy = item.contents[1].encode('utf-8')       
            if item.span.string.encode('utf-8') == "房本年限":
                   room_red_book = item.contents[1].encode('utf-8')       

        #print href, title, title_sub, price, unit_price, room_huxing, room_loucheng, room_fangxiang, room_zhuanxiu, room_size, room_has_year, xiaoqu_name, xiaoqu_href, area_qu, area_qu_sub, room_tihu, room_dianti, room_chanquan, room_now_buy, room_last_buy, room_shanping, room_red_book
        sql = 'set names utf8; insert into %s(href, title, title_sub, price, unit_price, room_huxing, room_loucheng, room_fangxiang, room_zhuanxiu, room_size, room_has_year, xiaoqu_name, xiaoqu_href, area_qu, area_qu_sub, room_tihu, room_dianti, room_chanquan, room_now_buy, room_last_buy, room_shanping, room_red_book) values("%s", "%s", "%s", %d, %d, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'%(table, href, title, title_sub, int(price), int(unit_price), room_huxing, room_loucheng, room_fangxiang, room_zhuanxiu, room_size, room_has_year, xiaoqu_name, xiaoqu_href, area_qu, area_qu_sub, room_tihu, room_dianti, room_chanquan, room_now_buy, room_last_buy, room_shanping, room_red_book)
        #print sql
        try:
            cur.execute(sql)
            cur.close()
            conn.commit()
            #send email
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    #conn.close()    

#需要请求一次得到总页数
insert_db(url%(init_page))
print total_page_num    
init_page=total_page_num/24*int(time.strftime('%H', time.localtime(time.time()))) + 1
for i in range(init_page, total_page_num+1):
    insert_db(url%(i))



#        for item in house.find_all('div', class_='houseInfo'):  
#            xiaoqu_href=item.a["href"]
#            xiaoqu_name=item.a.string
#            house_info = item.contents[len(item.contents)-1]
#        for item in house.find_all('div', class_='positionInfo'):  
#            year = item.contents[1]
#            diqu = item.a.string
#
#        print href, title, xiaoqu_href, xiaoqu_name, house_info, year, diqu
        
#print soup.prettify().encode('utf-8');

