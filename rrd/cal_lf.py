#!/bin/env python

import sys
import os
import time

from xml.etree import ElementTree
import urllib2
import rrdtool

sys.path.append("../")
import config
import MySQLdb
import time
import datetime 
import urlparse

def get_xml_child_value(element, name):
	child = element.find(name);
	if child is None:
		return None
	return child.text

def create_rrd(path, ts):
	print "create rrd " + path
	rrdtool.create(path, "--start", ts, "--step", "10", "DS:lf:GAUGE:120:0:1000000000", "RRA:AVERAGE:0.5:1:18000", "RRA:AVERAGE:0.5:10:1800", "RRA:AVERAGE:0.5:60:300");

def update_rrd(path, lf, ts):
	print "update rrd %s, value %d, time: %d"%( path, lf ,ts)
	rrdtool.update(path, "--template", "lf", "%d:%d"%(ts, lf) );

def draw_rrd(name, path, output):
	print "draw %s to %s"%( path, output )
	rrdtool.graph(output, "--vertical-label", "frame/sec"
				, "--start", "-2h"
				, "--lazy"
				, "--title", "loss frame of %s for web"%( name )
				, "-h", "200"
				, "-w", "600"
				, "DEF:lf=%s:lf:AVERAGE"%( path )
				, "LINE1:lf#0000FF"
				);

def drwa_rrd_weekly(name, path, output):
	print "draw %s to %s"%( path, output )
	rrdtool.graph(output, "--vertical-label", "bits/sec"
				, "--start", "-7d"
				, "-S", "3600"
				, "--lazy"
				, "--title", "Weekly loss frame of %s for web"%( name )
				, "-h", "200"
				, "-w", "600"
				, "DEF:lf=%s:lf:AVERAGE"%( path )
				, "LINE1:lf#0000FF"
				);

if __name__=="__main__":

	file = "/dev/shm/player.mm/access.log"
	min = "per_minute"
	file_fd = open(file, 'r')	

	now_t = int(datetime.datetime.now().strftime('%s'))
	last_str = datetime.datetime.fromtimestamp(now_t - 60).strftime('%Y:%H:%M')
	#print last_str

	for line in file_fd:
		if line.find(last_str) != -1 and line.find("heartbeat") != -1:
			#print line
			columns = line.split()
			#print columns[6]
			time_list = columns[3].split('[')
			#print time_list[1]
			x = datetime.datetime.strptime(time_list[1], '%d/%b/%Y:%H:%M:%S') 
			ts = int(time.mktime(x.timetuple()))
			#print ts
			parsed = urlparse.urlparse(columns[6])
			#print parsed
			params = urlparse.parse_qs(parsed.query, True)
			#print params 
			#print "\n"
		
			name = params['rid'][0]

			lf = params['lf'][0]
			
			print name + " " + lf

