#!/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

import MySQLdb
import config
import datetime
import web

LIMIT = 700
#meta_list = [   #determine order of display
#"meta_pub_overview"
#,"meta_live_overview"
#,"meta_pub_fail"
#,"meta_live_fail"
#,"meta_pub_inter"
#,"meta_live_inter"
#,"meta_live_time"
#]

class Handler:
    def GET(self):
        print "fuck"
        #t = web.input().get("t")
        dbmanager = MySQLdb.connect(config.mysql.host, config.mysql.user, config.mysql.passwd, config.mysql.db_name, config.mysql.port)
        cursor = dbmanager.cursor()
        yield '<html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n'
        yield '<title>报表</title>\n'
        yield '<link rel="stylesheet" href="http://%s/css/screen.css" type="text/css" media="screen">\n'%(config.IMAGE_HOST)
        yield '<style type="text/css"></style></head>\n'
        yield '<body>\n'
        yield '<div id="main">'
        #sql = "show tables like 'meta_%'"
        #print sql
        #cursor.execute(sql)
        #for t_name in cursor.fetchall():
        thead = "<thead><tr>"
        tbody = "<tbody>"
        tb_div = "<strong>%s</strong><br/>"%("asd")
        thead += '<th title="">%s</th>'%("saf")
        thead += "</tr></thead>"
        yield tb_div
        yield '<div id="chart_table" style="display: block;">'
        yield '<table>'
        yield thead
        tbody_sql = 'set names utf8; select * from lianjia_270_310 limit 10'
        print tbody_sql
        cursor.execute(tbody_sql)
        for b_res in cursor.fetchall():
            print b_res
            tbody += '<tr>'
            for val in b_res:
                tbody += '<td>' + str(val) + '</td>'
            tbody += '</tr>'
        tbody += '</tbody>\n</table>\n</div>\n<br/><br/><br/><br/>'
        
        yield tbody

        yield '</div>\n'
        #yield '<div class="footer">\n<a href>Designed by huanghao v0.1</a>\n</div>\n'
        yield '<script type="text/javascript" src="http://%s/css/jquery-1.7.1.min.js" charset="utf-8"></script>\n'%(config.IMAGE_HOST)
        yield '<link rel="stylesheet" href="http://%s/css/jquery.ui.all.css">\n'%(config.IMAGE_HOST)
        yield '<script type="text/javascript" src="http://%s/css/jquery.ui.core.js" charset="utf-8"></script>\n'%(config.IMAGE_HOST)
        yield '<script type="text/javascript" src="http://%s/css/jquery.ui.datepicker.js" charset="utf-8"></script>\n'%(config.IMAGE_HOST)
        yield '<script type="text/javascript" src="http://%s/css/highcharts.js" charset="utf-8"></script>\n'%(config.IMAGE_HOST)
        yield '<script type="text/javascript" src="http://%s/css/main.js" charset="utf-8"></script>\n'%(config.IMAGE_HOST)
        yield '</body>\n</html>\n'


if __name__ == "__main__":
    h = Handler()
    h.GET()
