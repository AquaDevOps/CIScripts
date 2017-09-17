# -*- coding: utf-8 -*-
#encoding=utf-8

import re
import httplib2
import datetime
from lxml import etree
from urllib import urlencode

REGEX_REPORT_PARAM = r'/ams/ams_weekly/WeeklyweeklyBrowse.do\?ctrl=weeklyweeklyvalueobject&action=Drilldown&param=(?P<param>\w+)'

def get_attr(attrs, name):
    for k, v in attrs:
        if name == k:
            return v
    return None

class Reporter:
    def __init__(self, host):
        self.http = httplib2.Http()
        self.host = host

    def login(self, username, password):
        url = self.host + "/ams/util/sys/login.do?method=login&username=%s&pwd=%s"
        resp, content = self.http.request(
            url % (username, password),
        )
        self.cookie = resp['set-cookie']

        resp, content = self.http.request(
            self.host + '/ams/ams_weekly/WeeklyweeklyBrowse.do?flag=true',
            headers={ 'Cookie': self.cookie }
        )
        # print(resp)

    def query_history(self, date_start, date_end = None):
        data = urlencode({
            'projectid':'',
            'formid':'frmSearch',
            'username':'',
            'projectname':'',
            'zhours':'',
            'begintime':date_start,
            'endtime':date_end or date_start,
            'btnSearch':'clicked',
            'btnLoad':'',
        })

        resp, content = self.http.request(
            self.host + '/ams/ams_weekly/WeeklyweeklyBrowse.do?flag=false',
            "POST",
            data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': str(len(data)),
                'Cookie': self.cookie,
            }
        )
        # print content

        data = {'reports':[]}

        html = etree.HTML(unicode(content, 'utf-8'))
        trs_report = html.xpath("//table[@class='lc']//table[@class='lcb']//table/tr[@class!='header']")

        params_report = list(set([
            re.search(REGEX_REPORT_PARAM, tr_report.xpath("td/a")[0].attrib['href']).group('param')
            for tr_report in trs_report
        ]))

        url = self.host + "/ams/ams_weekly/WeeklyweeklyDisplay.do?weeklyweeklyid=%s"

        for param_report in params_report:

            resp_report, resp_content = self.http.request(
                url % param_report,
                headers={ 'Cookie':self.cookie }
            )
            report = {}

            html = etree.HTML(unicode(resp_content, 'utf-8'))
            tag_script = html.xpath("//script[@type='text/javascript' and not(@src)]")[0].text
            tag_content = etree.tostring(html.xpath("//textarea[@name='weeklycontent']")[0], encoding="utf-8")
            tag_project = etree.tostring(html.xpath("//tr[@id='tr_attendanceprojectprojectname']/td[@class='fd']")[0], encoding="utf-8")

            time_start = re.search(r'var sst = \'(?P<time>[-\w: ,]+)\'', tag_script)
            time_end = re.search(r'var set = \'(?P<time>[-\w: ,]+)\'', tag_script)
            time_o_start = re.search(r'var osst = \'(?P<time>[-\w: ,]+)\'', tag_script)
            time_o_end = re.search(r'var oset = \'(?P<time>[-\w: ,]+)\'', tag_script)

            if time_start:
                time_start = [datetime.datetime.strptime(time, "%Y-%m-%d %H:%M") for time in time_start.group('time').split(',')[:-1]]
            else:
                time_start = []
            
            if time_end:
                time_end = [datetime.datetime.strptime(time, "%Y-%m-%d %H:%M") for time in time_end.group('time').split(',')[:-1]]
            else:
                time_end = []

            if time_o_start:
                time_o_start = [datetime.datetime.strptime(time, "%Y-%m-%d %H:%M") for time in time_o_start.group('time').split(',')[:-1]]
            else:
                time_o_start = []
            
            if time_o_end:
                time_o_end = [datetime.datetime.strptime(time, "%Y-%m-%d %H:%M") for time in time_o_end.group('time').split(',')[:-1]]
            else:
                time_o_end = []

            days = sorted(list(set([
                datetime.datetime(time.year, time.month, time.day).strftime("%Y-%m-%d")
                for time in time_start + time_o_start
            ])))

            calendar = { day : {} for day in days }
            
            for time in time_start:
                calendar[time.strftime("%Y-%m-%d")]['start'] = time.strftime("%H:%M")
            for time in time_end:
                calendar[time.strftime("%Y-%m-%d")]['end'] = time.strftime("%H:%M")
            for time in time_o_start:
                calendar[time.strftime("%Y-%m-%d")]['o_start'] = time.strftime("%H:%M")
            for time in time_o_end:
                calendar[time.strftime("%Y-%m-%d")]['o_end'] = time.strftime("%H:%M")
            report['days'] = days
            report['calendar'] = calendar
            report['param'] = param_report
            report['content'] = re.search(r'<[^<>]+>(?P<content>([^<>])+)<[^<>]+>', tag_content).group('content').strip().replace('&#13;', '')
            report['project'] = re.search(r'<[^<>]+>(?P<project>([^<>])+)<[^<>]+>', tag_project).group('project').strip().replace('&#13;', '')

            data['reports'].append(report)

        return data

    def print_history(self, date_start, date_end = None):
        data = self.query_history(date_start, date_end)
        
        data['reports'] = sorted(data['reports'], key=lambda x: x['days'][0])

        for report in data['reports']:
            # print('=' * 128)
            print('-' * 128)
            print('%36s : %s ' % (report['param'], report['project']))

            contents = report['content'].strip().splitlines()
            days = []

            for day in sorted(report['days'], key=lambda x: x):
                workday = report['calendar'][day]
                if workday.has_key('start'):
                    work = "%5s-%5s" % (workday['start'], workday['end'])
                else:
                    work = ' ' * 11
                if workday.has_key('o_start'):
                    over = "%5s-%5s" % (workday['o_start'], workday['o_end'])
                else:
                    over = ' ' * 11
                days.append("%s %s %s" % (day, work, over))

            count = max(len(contents), len(days))
            contents.extend([''] * (count - len(contents)))
            days.extend([''] * (count - len(days)))

            for i in range(count):
                print('%36s : %s ' % (days[i], contents[i]))
            print('')

    def log_worklog(self, content, date, time_start='', time_end='', time_o_start='', time_o_end=''):
        data = urlencode({
            'projectid':'2c90827052e7b61401535a546c0e0609',
            'formid':'frmCreate',
            'projectname':'辰安公共安全云平台V2.0.0',
            'weeklycontent':content.strip(),
            'starttime':time_start and '%s %s' % (date, time_start),
            'endtime':  time_end and '%s %s' % (date, time_end),
            'startstr': time_start and '%s %s' % (date, time_start),
            'endstr':   time_end and '%s %s' % (date, time_end),
            'iscomplete':'100',
            'overtimestart':time_o_start and '%s %s' % (date, time_o_start),
            'overtimeend':  time_o_end and '%s %s' % (date, time_o_end),
            'overstartstr': time_o_start and '%s %s' % (date, time_o_start),
            'overendstr':   time_o_end and '%s %s' % (date, time_o_end),
            'btnSave':'clicked',
            'otherprojectid': '',
            'plancontent': '',
            'problem': '',
            'remark': '',
            'btnAdd': '',
            'btnBack': '',
        })
        
        resp, content = self.http.request(
            self.host + '/ams/ams_weekly/WeeklyweeklyAdd.do',
            "POST", data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': str(len(data)),
                'Referer': 'http://192.168.29.31:7003/ams/ams_weekly/WeeklyweeklyAdd.do',
                'Cookie': self.cookie,
                'Host': '192.168.29.31:7003',
            }
        )
        print(resp)
        # print(content)

    def log_worklogs(self, log_content, log_datetime=None):
        content_lines = [line.strip() for line in log_content.strip().splitlines()]
        if log_datetime:
            datetime_lines = [line.strip() for line in log_datetime.strip().splitlines()]

            for index in range(0, len(content_lines)):
                # print(datetime_lines[index])
                # print(content_lines[index])
                datetime_parts = datetime_lines[index].split(' ') + ['']

                # print('%8s %11s %11s %s' % (datetime_parts[0], datetime_parts[1], datetime_parts[2], content_lines[index]))
                # print('%s-%s-%s' % (datetime_parts[0][0:4], datetime_parts[0][4:6], datetime_parts[0][6:8]))
                # print(datetime_parts[1][0:5])
                # print(datetime_parts[1][6:11])
                # print(datetime_parts[2][0:5])
                # print(datetime_parts[2][6:11])
                self.log_worklog(
                    date='%s-%s-%s' % (datetime_parts[0][0:4], datetime_parts[0][4:6], datetime_parts[0][6:8]),
                    time_start=datetime_parts[1][0:5],
                    time_end=datetime_parts[1][6:11],
                    time_o_start=datetime_parts[2][0:5],
                    time_o_end=datetime_parts[2][6:11],
                    content=content_lines[index]
                )
