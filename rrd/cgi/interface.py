#!/bin/env python
# -*- coding: gb18030 -*-

import sys
import web

import online
import server

urls = ( '/monitor/online', 'online.Handler' 
	 , '/monitor/server', 'server.Handler'
	 , '/monitor/flash', 'flash.Handler'
	)

app = web.application(urls, globals(), autoreload=True)
if __name__ == '__main__':
        app.run()
        #print app.request("/cloudtranscode/cgi/iss?g=E2EDB4213A0DAAAAA606E2D5B29AF9928EB7E3FF&nt=0").data
