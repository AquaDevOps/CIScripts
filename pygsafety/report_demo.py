# -*- coding: utf-8 -*-
#encoding=utf-8

import json
from report_lib import Reporter

host_work = 'http://192.168.29.31:7003'

reporter = Reporter(host_work)
reporter.login('username', 'password')

# reporter.printHistory('2017-05-15', '2017-05-21')
# print('===== before =====')

reporter.logWorklog(date='2017-06-26', time_start= '09:00', time_end= '18:00', time_o_start= '20:30', time_o_end= '21:30', content='''
    Jenkins构建队列云平台环境调试
    一张图项目Sonarqube代码扫描规则评审并给项目负责人讲解
    ''')
reporter.logWorklog(date='2017-06-27', time_start= '09:00', time_end= '18:00', time_o_start= '18:00', time_o_end= '21:20', content='云平台项目构建中遇到的依赖缺失故障的排查与修复')
reporter.logWorklog(date='2017-06-21', time_start= '09:00', time_end= '18:00', time_o_start= '18:00', time_o_end= '21:00', content='Jenkins构建队列调度服务设计与实现')
reporter.logWorklog(date='2017-06-22', time_start= '09:00', time_end= '18:00', time_o_start= '18:00', time_o_end= '22:30', content='Jenkins构建队列调度动态同步设计与实现')
reporter.logWorklog(date='2017-06-23', time_start= '09:00', time_end= '18:00', time_o_start= '18:00', time_o_end= '21:20', content='Jenkins构建脚本动态多模块功能调试及实现')
reporter.logWorklog(date='2017-06-24', time_start= '',      time_end= '',      time_o_start= '11:00', time_o_end= '18:20', content='软件版本发布流程设计')
reporter.logWorklog(date='2017-06-25', time_start= '',      time_end= '',      time_o_start= '10:00', time_o_end= '20:00', content='nginx调优及在线文档路径设计')

print('===== after ======')
reporter.printHistory('2017-06-19', '2017-06-25')

# http://192.168.29.31:7003/ams/ams_weekly/WeeklyweeklyEdit.do?weeklyweeklyid=40289d9f5981549c015c49b1a8f66998