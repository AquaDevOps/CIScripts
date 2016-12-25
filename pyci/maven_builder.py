# -*- coding: utf-8 -*-
#encoding=utf-8
import os, sys, json, getopt

sys.path.append(os.path.dirname(__file__))

from libs import ProcessUtils
from libs import MavenUtils
from libs import FileUtils

pom = MavenUtils.Pom.from_str('com.gsafety.sample:sample-parent:0.0.1-Snapshot')
pom.path = 'E:/svn/CFWTest/trunk/sample-parent'
pom.package = 'test'

for line in '''
com.fasterxml.jackson.core:jackson-databind:2.5.3
'''.strip().splitlines():
    cmd = MavenUtils.maven_get(MavenUtils.Pom.from_str(line.strip()))
    print('cmd:%s' % cmd)
    ProcessUtils.process(cmd)
    print('\n\n\n')
'''
log4j:log4j:1.2.17
javax.websocket.server:websocket-api:1.1
org.apache.maven.plugins:maven-downloader-plugin:1.0
avalon-framework:avalon-framework:4.1.3
commons-logging:commons-logging:1.1
org.apache.maven.plugins:maven-archetype-plugin:2.4
'''

# cmd = MavenUtils.maven_generate(pom)
# print('cmd:%s' % cmd)

# ProcessUtils.process(cmd)