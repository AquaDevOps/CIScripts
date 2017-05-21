# -*- coding: utf-8 -*-
#encoding=utf-8

from report_lib import Reporter

host_work = 'http://192.168.29.31:7003'
host_home = 'http://106.37.227.19:7003'

reporter = Reporter(host_home)
reporter.login('*******', '******')
reporter.getHistory('2017-05-21')