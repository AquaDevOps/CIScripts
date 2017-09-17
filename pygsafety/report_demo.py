# -*- coding: utf-8 -*-
#encoding=utf-8

import json
from report_lib import Reporter

host_work = 'http://192.168.29.31:7003'

reporter = Reporter(host_work)
# reporter.login('username', 'password')

print('===== before =====')
reporter.log_worklogs(
    log_content='''
    你周一干了啥
    你周二干了啥
    你周三干了啥
    你周四干了啥
    你周五干了啥
    你周六干了啥
    你周七干了啥
    ''',
    log_datetime='''
    20170911 09:00-18:00 18:00-21:50
    20170912 09:00-18:00 18:00-21:30
    20170913 09:00-18:00 18:00-22:00
    20170914 09:00-18:00 18:00-21:30
    20170915 09:00-18:00
    20170916  18:00-21:30
    20170917  11:30-21:00
    '''
)
print('===== after ======')
reporter.print_history('2017-09-11', '2017-09-17')

# http://192.168.29.31:7003/ams/ams_weekly/WeeklyweeklyEdit.do?weeklyweeklyid=40289d9f5981549c015c49b1a8f66998