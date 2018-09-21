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
	rrdtool.create(path, "--start", ts, "--step", "10", "DS:bwin:GAUGE:120:0:1000000000","DS:video:GAUGE:120:0:1000000000", "DS:audio:GAUGE:120:0:1000000000", "RRA:AVERAGE:0.5:1:18000", "RRA:AVERAGE:0.5:10:1800", "RRA:AVERAGE:0.5:60:300");

def update_rrd(path, bwin, video, audio, ts):
	print "update rrd %s, value %d %d %d, time: %d"%( path, bwin, video, audio ,ts)
	rrdtool.update(path, "--template", "bwin:video:audio", "%d:%d:%d:%d"%(ts, bwin, video, audio) );

def draw_rrd(name, path, output):
	print "draw %s to %s"%( path, output )
	rrdtool.graph(output, "--vertical-label", "bits/sec"
				, "--start", "-2h"
				, "--lazy"
				, "--title", "Bandwidth of %s for web"%( name )
				, "-h", "200"
				, "-w", "600"
				, "DEF:bwin=%s:bwin:AVERAGE"%( path )
				, "DEF:video=%s:video:AVERAGE"%( path )
				, "DEF:audio=%s:audio:AVERAGE"%( path )
				, "COMMENT:                     now        average        max        min \\n"
				, "LINE1:bwin#0000FF:total bitrate"
				, "GPRINT:bwin:LAST: %8.2lf"
				, "GPRINT:bwin:AVERAGE: %8.2lf"
				, "GPRINT:bwin:MAX: %8.2lf"
				, "GPRINT:bwin:MIN: %8.2lf"

				, "COMMENT:\\n"
				, "LINE1:video#4A4F69:video bitrate"
				, "GPRINT:video:LAST: %8.2lf"
				, "GPRINT:video:AVERAGE: %8.2lf"
				, "GPRINT:video:MAX: %8.2lf"
				, "GPRINT:video:MIN: %8.2lf"

				, "COMMENT:\\n"
				, "LINE1:audio#00FF00:audio bitrate"
				, "GPRINT:audio:LAST: %8.2lf"
				, "GPRINT:audio:AVERAGE: %8.2lf"
				, "GPRINT:audio:MAX: %8.2lf"
				, "GPRINT:audio:MIN: %8.2lf"

				);

def drwa_rrd_weekly(name, path, output):
	print "draw %s to %s"%( path, output )
	rrdtool.graph(output, "--vertical-label", "bits/sec"
				, "--start", "-7d"
				, "-S", "3600"
				, "--lazy"
				, "--title", "Weekly Bandwidth of %s for web"%( name )
				, "-h", "200"
				, "-w", "600"
				, "DEF:bwin=%s:bwin:AVERAGE"%( path )
				, "DEF:video=%s:video:AVERAGE"%( path )
				, "DEF:audio=%s:audio:AVERAGE"%( path )
				, "LINE1:bwin#0000FF"
				, "LINE1:video#DC143C"
				, "LINE1:audio#7CFC00"
				);

if __name__=="__main__":

	file = "/dev/shm/player.mm/access_pub.log"
	file_fd = open(file, 'r')	

	now_t = int(datetime.datetime.now().strftime('%s'))
	last_str = datetime.datetime.fromtimestamp(now_t - 60).strftime('%Y:%H:%M')
	print last_str

	for line in file_fd:
		if line.find(last_str) != -1 and line.find("heartbeat") != -1:
			#print line
			columns = line.split()
			print columns[6]
			time_list = columns[3].split('[')
			print time_list[1]
			x = datetime.datetime.strptime(time_list[1], '%d/%b/%Y:%H:%M:%S') 
			ts = int(time.mktime(x.timetuple()))
			print ts
			parsed = urlparse.urlparse(columns[6])
			print parsed
			params = urlparse.parse_qs(parsed.query, True)
			print params
		
			name = "room_" + params['rid'][0]
			path = "%s/data/%s_web.rrd"%(config.HOME, name)	
			output="%s/html/mrtg/%s_web.png"%( config.HOME, name )
			output_weekly="%s/html/mrtg/weekly/%s_web.png"%( config.HOME, name )
			if os.access(path, os.F_OK) is False:
				create_rrd(path, str(ts-1))
		
			bwin = int(params['tbr'][0])
			video = int(params['vbr'][0])
			audio = int(params['abr'][0])
			bwin = bwin * 8
			video = video * 8 
			audio = audio * 8
			update_rrd(path, bwin, video, audio, ts);
			draw_rrd(name, path, output);
			drwa_rrd_weekly(name, path, output_weekly)
