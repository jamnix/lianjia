#!/bin/env python
# -*- encoding: gb18030 -*-

import sys
import os
import time

import rrdtool
import MySQLdb

sys.path.append("../")
import config

def get_xml_child_value(element, name):
	child = element.find(name);
	if child is None:
		return None
	return child.text

def create_rrd(path):
	print "create rrd " + path
	rrdtool.create(path, "--step", "60"
			, "DS:online:GAUGE:120:0:1000000000"
			, "RRA:AVERAGE:0.5:1:18000" # per 1min,   total 300h
			, "RRA:AVERAGE:0.5:10:1800" # per 10mins, total 300h
			, "RRA:AVERAGE:0.5:60:300"  # per 1h,     total 300h
			, "RRA:AVERAGE:0.5:120:372" # per 2h,     total 1mon
			, "RRA:AVERAGE:0.5:1440:365" # per 1d,    total 1year
			); 

def update_rrd(path, value):
	print "update rrd %s, value %d"%( path, value )
	rrdtool.update(path, "--template", "online", "N:%d"%(value) );

def draw_rrd(title, path, output):
	print "draw %s to %s"%( path, output )
	rrdtool.graph(output, "--vertical-label", "users"
				, "--start", "-3h"
				, "--title", title
				, "--lazy"
				, "--font", "TITLE:0:Cursive"
				, "-h", "200"
				, "-w", "600"
				, "DEF:bwin=%s:online:AVERAGE"%( path ), "LINE1:bwin#0000FF");

def draw_rrd_weekly(title, path, output):
	print "draw %s to %s"%( path, output )
	rrdtool.graph(output, "--vertical-label", "users"
				, "--start", "-7d"
				, "-S", "3600"
				, "--lazy"
				, "--title", title
				, "-h", "200"
				, "-w", "600"
				, "DEF:bwin=%s:online:AVERAGE"%( path ), "LINE1:bwin#0000FF");

def draw_rrd_monthly(title, path, output):
        print "draw %s to %s"%( path, output )
        rrdtool.graph(output, "--vertical-label", "users"
                                , "--start", "-31d"
                                , "-S", "7200"
                                , "--title", title
                                , "-h", "200"
                                , "-w", "600"
                                , "DEF:bwin=%s:online:AVERAGE"%( path ), "LINE1:bwin#0000FF");

def draw_rrd_yearly(title, path, output):
        print "draw %s to %s"%( path, output )
        rrdtool.graph(output, "--vertical-label", "users"
                                , "--start", "-365d"
                                , "-S", "86400"
                                , "--lazy"
                                , "--title", title
                                , "-h", "200"
                                , "-w", "600"
                                , "DEF:bwin=%s:online:AVERAGE"%( path ), "LINE1:bwin#0000FF");

def draw_all(online):
	name = "online"
	path = "%s/data/%s.rrd"%( config.HOME, name )
	output="%s/html/mrtg/%s.png"%( config.HOME, name )
	output_weekly="%s/html/mrtg/%s_weekly.png"%( config.HOME, name )
	output_monthly="%s/html/mrtg/%s_monthly.png"%( config.HOME, name )
	output_yearly="%s/html/mrtg/%s_yearly.png"%( config.HOME, name )
	if os.access(path, os.F_OK) is False:
		create_rrd(path);
	update_rrd(path, online);
	draw_rrd("Realtime Online Users", path, output);
	draw_rrd_weekly("Weekly Online Users", path, output_weekly);
	draw_rrd_monthly("Monthly Online Users", path, output_monthly);
	draw_rrd_yearly("Yearly Online Users", path, output_yearly);

if __name__=="__main__":
	mysql = MySQLdb.connect(host=config.RtmpStatMYSQL.host
				, user=config.RtmpStatMYSQL.user
				, passwd=config.RtmpStatMYSQL.password
				, db="rtmp_info")
	cursor = mysql.cursor()
	cursor.execute("select sum(num) from rtmp_stat")
	online, = cursor.fetchone()
	cursor.close()
	mysql.close()
	print online
	draw_all( online );
