#!/bin/env python
# -*- coding: gb18030 -*-

import sys
import urllib2
from xml.etree import ElementTree
import web

sys.path.append("../")
import config

def get_xml_child_value(element, name):
        child = element.find(name);
        if child is None:
                return None
        return child.text

class Handler:
	def GET(self):
		yield '<html>\n'
		yield '<head>\n'
		yield '<title> Online Rooms MRTG </title>\n'
		yield '<meta http-equiv="Refresh" content="60">\n'
		yield '<meta http-equiv="Cache-Control" content="no-cache">\n'
		yield '<meta http-equiv="Pragma" content="no-cache">\n'
		yield '<meta http-equiv="Content-Type" content="text/html; charset=GB2312">\n'
		yield '<link rel="stylesheet" href="http://%s/comm.css" type="text/css" />\n'%( config.IMAGE_HOST )
		yield '</head>\n'
		yield '<body>\n'
		yield '<div class="main_title">Online Rooms MRTG</div>\n'
		yield '<div id="main_list">\n'
		for h in config.HOSTS:
			yield '<div>\n'
			yield '<p class="sub_title">%s</p>\n'%( h )
        		url = "http://%s/stat"%( h )
       			try:
                		xml = urllib2.urlopen(url).read();
        		except urllib2.HTTPError as e:
                		print "url error, code %d"%( e.getcode() )
                		continue
			print h
        		root = ElementTree.fromstring(xml);
        		eapps = root.findall("server/application");
        		for eapp in eapps:
                		name = get_xml_child_value(eapp, "name")
                		if name is None or name!=config.APPNAME:
                        		continue
                		estreams = eapp.findall("live/stream")
                		for estream in estreams:
                        		name = get_xml_child_value(estream, "name");
					print name
					yield '<p>\n'
					yield '<div class="image_bg">\n'
					yield '<div>%s</div>\n'%( name )
					yield '<div float:left><a href="http://%s/mrtg/weekly/%s.png" target="_blank" alt="Weekly Bandwith"><img src="http://%s/mrtg/%s.png"></a></div>\n'%( config.IMAGE_HOST, name, config.IMAGE_HOST, name )
					yield '<div float:left><a href="http://%s/mrtg/weekly/%s_web.png" target="_blank" alt="Weekly Bandwith"><img src="http://%s/mrtg/%s_web.png"></a></div>\n'%( config.IMAGE_HOST, name, config.IMAGE_HOST, name )
					yield '<div float:left><a href="http://%s/mrtg/weekly/%s_web_lf.png" target="_blank" alt="Weekly Bandwith"><img src="http://%s/mrtg/%s_web_lf.png"></a></div>\n'%( config.IMAGE_HOST, name, config.IMAGE_HOST, name )
					yield '</div>\n'
					yield '</p>\n'
                		break
			yield '</div>\n'

		yield '</div></body>\n'
		yield '</html>'
