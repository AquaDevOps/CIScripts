# -*- coding: utf-8 -*-
#encoding=utf-8

import re
import json
import urllib2
import httplib2
import cookielib
from urllib import urlencode
from HTMLParser import HTMLParser
from lxml import etree

def get_attr(attrs, name):
    for k, v in attrs:
        if name == k:
            return v
    return None

class WorklogDetailParse(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = {}
        self.key = None

    def get_data(self):
        return self.data

    def handle_starttag(self, tag, attrs):
        if 'script' == tag and None == get_attr(attrs, 'src'):
            self.key = 'script'
        if 'textarea' == tag and 'weeklycontent' == get_attr(attrs, 'name'):
            self.key = 'content'
        pass

    def handle_data(self, data):
        if None != self.key:
            self.data[self.key] = data
            self.key = None
        pass

    def handle_endtag(self, tag):
        pass

class WorklogParamParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.depth = 0
        self.flag = False
        self.parse = False
        self.params = []

    def get_params(self):
        return list(set(self.params))

    def handle_starttag(self, tag, attrs):
        def get_attr(attrs, name):
            for k, v in attrs:
                if name == k:
                    return v
            return None

        self.depth += 1

        if ('table' == tag) and ('lcb' == get_attr(attrs, 'class')):
            self.flag = self.depth
        
        if self.flag:
            if 'a' == tag:
                href = get_attr(attrs, 'href')
                result = re.search(r'/ams/ams_weekly/WeeklyweeklyBrowse.do\?ctrl=weeklyweeklyvalueobject&action=Drilldown&param=(?P<param>\w+)', href)
                if result:
                    param = result.group('param')
                    self.params.append(param)
                
            pass

    def handle_data(self, data):
        pass

    def handle_endtag(self, tag):
        if self.depth == self.flag:
            self.flag = False

        self.depth -= 1
        pass
base_host = 'http://192.168.29.31:7003'
base_host = 'http://106.37.227.19:7003'

login_context = "/ams/util/sys/login.do?method=login&username=%s&pwd=%s"

http = httplib2.Http()

resp, content = http.request(
    base_host + login_context % ('xuwenzhe', 'alexander'),
    headers={
        'Accept': 'application/json'
    }
)
cookie = resp['set-cookie']

# 登录主页
# resp, content = http.request(
#   base_host + '/ams/' + re.search(r'toUrl:\'(?P<url>[\w/.]+)', content).group('url'),
#   headers={ 'Cookie': cookie }
# )

# 日报浏览
# resp, content = http.request(
#   base_host + '/ams/' + 'ams_weekly/WeeklyweeklyBrowse.do?flag=true',
#   headers={ 'Cookie': cookie }
# )

# open('output.txt', 'w+').write(content)

# 历史日报
def getHistory(begin, end):
    data = urlencode({
        'projectid':'',
        'formid':'frmSearch',
        # 可以把名字写上
        'username':'',
        'projectname':'',
        'zhours':'',
        'begintime':begin,
        'endtime':end,
        'btnSearch':'clicked',
        'btnLoad':'',
    })
    resp, content = http.request(
        base_host + '/ams/' + 'ams_weekly/WeeklyweeklyBrowse.do?flag=false',
        "POST", data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': str(len(data)),
            'Referer': 'http://192.168.29.31:7003/ams/ams_weekly/WeeklyweeklyAdd.do',
            'Cookie': cookie,
        }
    )
    print(resp)

    # print(content)
    historyParser = WorklogParamParser()
    historyParser.feed(content)
    params = historyParser.get_params()

    for param in params:
        resp, content = getHistoryDetail(param)

        html = etree.HTML(content)

        script = html.xpath("//script[@type='text/javascript' and not(@src)]")[0].text
        # print(script[0].text)

        detailParser = WorklogDetailParse()
        detailParser.feed(content)
        data = detailParser.get_data()

        # print(data)
        # print(data['script'])
        start_time = re.search(r'var sst = \'(?P<time>[-\w: ,]+)\'', script).group('time').split(',')[:-1]
        end_time = re.search(r'var set = \'(?P<time>[-\w: ,]+)\'', script).group('time').split(',')[:-1]

        over_start_time = re.search(r'var osst = \'(?P<time>[-\w: ,]+)\'', script).group('time').split(',')[:-1]
        over_end_time = re.search(r'var oset = \'(?P<time>[-\w: ,]+)\'', script).group('time').split(',')[:-1]

        print(start_time)
        print(end_time)
        print(over_start_time)
        print(over_end_time)
        print(data['content'].strip())

        html = etree.HTML(content)

        

# <script type="text/javascript">

        

def getHistoryDetail(param):
    resp, content = http.request(
        base_host + "/ams/ams_weekly/WeeklyweeklyDisplay.do?weeklyweeklyid=%s" % param,
        headers={
            'Cookie': cookie,
        }
    )
    return resp, content



def logWorkLog(content, starttime, endtime, overstarttime, overendtime):
    data = urlencode({
        'projectid':'2c90827052e7b61401535a546c0e0609',
        'formid':'frmCreate',
        'projectname':'辰安公共安全云平台V2.0.0',
        'weeklycontent':content,
        'starttime':starttime,
        'endtime':  endtime,
        'startstr': starttime,
        'endstr':   endtime,
        'iscomplete':'100',
        'overtimestart':overstarttime,
        'overtimeend':  overendtime,
        'overstartstr': overstarttime,
        'overendstr':   overendtime,
        'btnSave':'clicked',
        'otherprojectid': '',
        'plancontent': '',
        'problem': '',
        'remark': '',
        'btnAdd': '',
        'btnBack': '',
    })
    resp, content = http.request(
        base_host + '/ams/' + 'ams_weekly/WeeklyweeklyAdd.do',
        "POST", data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': str(len(data)),
            'Referer': 'http://192.168.29.31:7003/ams/ams_weekly/WeeklyweeklyAdd.do',
            'Cookie': cookie,
        }
    )
    print(resp)

getHistory(begin='2017-05-15', end='2017-05-20')

# logWorkLog(
#   content='''
# 整理协同开发环境文档
# ''',
#   starttime =     '2017-05-20 09:00',
#   endtime =       '2017-05-20 18:00',
#   overstarttime = '2017-05-20 18:00',
#   overendtime =   '2017-05-20 20:20',
# )