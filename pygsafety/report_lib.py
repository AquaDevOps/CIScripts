# -*- coding: utf-8 -*-
#encoding=utf-8

import httplib2
from urllib import urlencode
from lxml import etree

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

        print(resp)
        return resp, content

    def getHistory(self, startdate, enddate = None):
        data = urlencode({
            'projectid':'',
            'formid':'frmSearch',
            'username':'',
            'projectname':'',
            'zhours':'',
            'begintime':startdate,
            'endtime':enddate or startdate,
            'btnSearch':'clicked',
            'btnLoad':'',
        })

        resp, content = self.http.request(
            self.host + '/ams/ams_weekly/WeeklyweeklyBrowse.do?flag=false',
            "POST",
            data,
            headers={
                # 'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': str(len(data)),
                # 'Referer': 'http://192.168.29.31:7003/ams/ams_weekly/WeeklyweeklyAdd.do',
                'Cookie': self.cookie,
            }
        )
        print resp
        return resp, content