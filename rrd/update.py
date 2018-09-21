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
	rrdtool.create(path, "--step", "60", "DS:bwin:GAUGE:120:0:1000000000", "RRA:AVERAGE:0.5:1:18000", "RRA:AVERAGE:0.5:10:1800", "RRA:AVERAGE:0.5:60:300");

def update_rrd(path, value):
	print "update rrd %s, value %d"%( path, value )
	rrdtool.update(path, "--template", "bwin", "N:%d"%(value) );

def draw_rrd(name, path, output):
	print "draw %s to %s"%( path, output )
	rrdtool.graph(output, "--vertical-label", "bits/sec"
				, "--start", "-2h"
				, "--lazy"
				, "--title", "Bandwidth of %s"%( name )
				, "-h", "200"
				, "-w", "600"
				, "DEF:bwin=%s:bwin:AVERAGE"%( path ), "LINE1:bwin#0000FF");

def drwa_rrd_weekly(name, path, output):
	print "draw %s to %s"%( path, output )
	rrdtool.graph(output, "--vertical-label", "bits/sec"
				, "--start", "-7d"
				, "-S", "3600"
				, "--lazy"
				, "--title", "Weekly Bandwidth of %s"%( name )
				, "-h", "200"
				, "-w", "600"
				, "DEF:bwin=%s:bwin:AVERAGE"%( path ), "LINE1:bwin#0000FF");

if __name__=="__main__":
	for h in config.HOSTS:
		print ""
		print h
		url = "http://%s/stat"%( h )
		try:
			xml = urllib2.urlopen(url).read();
		except urllib2.HTTPError as e:
			print "url error, code %d"%( e.getcode() )
			continue
		root = ElementTree.fromstring(xml);
		eapps = root.findall("server/application");
		for eapp in eapps:
			name = get_xml_child_value(eapp, "name")
			if name is None or name!=config.APPNAME:
				continue
			estreams = eapp.findall("live/stream")
			for estream in estreams:
				name = get_xml_child_value(estream, "name");
				bwin = get_xml_child_value(estream, "bwin");
				path="%s/data/%s.rrd"%( config.HOME, name )
				output="%s/html/mrtg/%s.png"%( config.HOME, name )
				output_weekly="%s/html/mrtg/weekly/%s.png"%( config.HOME, name )
				if os.access(path, os.F_OK) is False:
					create_rrd(path);
				update_rrd(path, int(bwin));
				draw_rrd(name, path, output);
				drwa_rrd_weekly(name, path, output_weekly);
			break
