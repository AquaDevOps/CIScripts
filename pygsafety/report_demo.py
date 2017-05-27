# -*- coding: utf-8 -*-
#encoding=utf-8

import json
from report_lib import Reporter

host_work = 'http://192.168.29.31:7003'
host_home = 'http://106.37.227.19:7003'

reporter = Reporter(host_work)
reporter.login('******', '******')
# reporter.printHistory('2017-05-15', '2017-05-21')
print('===== before =====')

reporter.logWorklog(
    content='''
    整理代码检查规则
    ''',
    time_start=     '2017-05-27 09:00',
    time_end=       '2017-05-27 18:00',
    time_o_start=   '2017-05-27 18:00',
    time_o_end=     '2017-05-27 20:00'
)

print('===== after ======')
reporter.printHistory('2017-05-22', '2017-05-28')

# http://192.168.29.31:7003/ams/ams_weekly/WeeklyweeklyEdit.do?weeklyweeklyid=40289d9f5981549c015c49b1a8f66998