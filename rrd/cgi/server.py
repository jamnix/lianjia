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


def print_image_line(title, name):
		yield '<p>\n'
		yield '<div class="image_bg">\n'
		yield '<div>%s</div>\n'%( title )
		yield '<div><a href="http://%s/mrtg/server/%s_weekly.png" target="_blank" alt="Weekly Bandwith">\
			<img src="http://%s/mrtg/server/%s.png"></a></div>\n'\
			%( config.IMAGE_HOST, name, config.IMAGE_HOST, name )
		yield '</div>\n'
		yield '</p>\n'

class Handler:
	def GET(self):
		yield '<html>\n'
		yield '<head>\n'
		yield '<title> RTMP server MRTG </title>\n'
		yield '<meta http-equiv="Refresh" content="60">\n'
		yield '<meta http-equiv="Cache-Control" content="no-cache">\n'
		yield '<meta http-equiv="Pragma" content="no-cache">\n'
		yield '<meta http-equiv="Content-Type" content="text/html; charset=GB2312">\n'
		yield '<link rel="stylesheet" href="http://%s/comm.css" type="text/css" />\n'%( config.IMAGE_HOST )
		yield '</head>\n'
		yield '<body>\n'
		yield '<div class="main_title">RTMP Server MRTG</div>'
		yield '<div id="main_list">\n'

		yield '<div>\n'
		for line in print_image_line("TOTAL", "all_rtmp_server"):
			yield line
		yield '</div>\n'

		yield '<div>\n'
		for h in config.HOSTS:
			name = h.split(".")[0]
			for line in print_image_line(name, name):
				yield line
		yield '</div>\n'

		yield '</div></body>\n'
		yield '</html>'
