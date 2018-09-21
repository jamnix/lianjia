#!/bin/env python

import sys
import os
import time

from xml.etree import ElementTree
import urllib2
import rrdtool

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
			, "DS:bwin:GAUGE:120:0:1000000000"
			, "RRA:AVERAGE:0.5:1:18000" # per 1min,   total 300h
			, "RRA:AVERAGE:0.5:10:1800" # per 10mins, total 300h
			, "RRA:AVERAGE:0.5:60:300"  # per 1h,     total 300h
			, "RRA:AVERAGE:0.5:120:372" # per 2h,     total 1mon
			, "RRA:AVERAGE:0.5:1440:365" # per 1d,    total 1year
			); 

def update_rrd(path, value):
	print "update rrd %s, value %d"%( path, value )
	rrdtool.update(path, "--template", "bwin", "N:%d"%(value) );

def draw_rrd(name, path, output):
	print "draw %s to %s"%( path, output )
	rrdtool.graph(output, "--vertical-label", "bits/sec"
				, "--start", "-3h"
				, "--lazy"
				, "--title", "Bandwidth of %s"%( name )
				, "-h", "200"
				, "-w", "600"
				, "DEF:bwin=%s:bwin:AVERAGE"%( path ), "LINE1:bwin#0000FF");

def draw_rrd_weekly(name, path, output):
	print "draw %s to %s"%( path, output )
	rrdtool.graph(output, "--vertical-label", "bits/sec"
				, "--start", "-7d"
				, "-S", "1800"
				, "--lazy"
				, "--title", "Weekly Bandwidth of %s"%( name )
				, "-h", "200"
				, "-w", "600"
				, "DEF:bwin=%s:bwin:AVERAGE"%( path ), "LINE1:bwin#0000FF");

def draw_rrd_monthly(name, path, output):
        print "draw %s to %s"%( path, output )
        rrdtool.graph(output, "--vertical-label", "bits/sec"
                                , "--start", "-31d"
                                , "-S", "7200"
                                , "--lazy"
                                , "--title", "Monthly Bandwidth of %s"%( name )
                                , "-h", "200"
                                , "-w", "600"
                                , "DEF:bwin=%s:bwin:AVERAGE"%( path ), "LINE1:bwin#0000FF");

def draw_rrd_yearly(name, path, output):
        print "draw %s to %s"%( path, output )
        rrdtool.graph(output, "--vertical-label", "bits/sec"
                                , "--start", "-365d"
                                , "-S", "86400"
                                , "--lazy"
                                , "--title", "Yearly Bandwidth of %s"%( name )
                                , "-h", "200"
                                , "-w", "600"
                                , "DEF:bwin=%s:bwin:AVERAGE"%( path ), "LINE1:bwin#0000FF");

def draw_all(name, bwin):
	path = "%s/data/%s.rrd"%( config.HOME, name )
	output="%s/html/mrtg/server/%s.png"%( config.HOME, name )
	output_weekly="%s/html/mrtg/server/%s_weekly.png"%( config.HOME, name )
	output_monthly="%s/html/mrtg/server/%s_monthly.png"%( config.HOME, name )
	output_yearly="%s/html/mrtg/server/%s_yearly.png"%( config.HOME, name )
	if os.access(path, os.F_OK) is False:
		create_rrd(path);
	update_rrd(path, bwin);
	draw_rrd(name, path, output);
	draw_rrd_weekly(name, path, output_weekly);
	draw_rrd_monthly(name, path, output_monthly);
	draw_rrd_yearly(name, path, output_yearly);

if __name__=="__main__":
	total_bwin = 0;
	for h in config.HOSTS:
		name = h.split(".")[0]
		url = "http://%s/stat"%( h )
		try:
			xml = urllib2.urlopen(url).read();
		except urllib2.HTTPError as e:
			print "url error, code %d"%( e.getcode() )
			continue
		root = ElementTree.fromstring(xml);
		bwin = get_xml_child_value( root, "bwin" );
		if bwin is None:
			continue
		print name, bwin
		total_bwin += int(bwin)
		draw_all( name, int(bwin) )
	draw_all( "all_rtmp_server", total_bwin );
