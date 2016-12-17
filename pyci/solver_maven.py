# -*- coding: utf-8 -*-
#encoding=utf-8
import os, sys, json, getopt

sys.path.append(os.path.dirname(__file__))

from libs import ProcessUtils
from libs import MavenUtils
from libs import FileUtils

#################################
#                               #
# Solve Maven Compile sequence  #
#                               #
#################################


if 1 == len(sys.argv):
    sys.argv = [sys.argv[0]]

    cmd = u'''
    --target=com.gsafety.anjian:anjian
    --root=E:/svn/国家安全生产应急联动与智能决策系统
    --include=应急一张图build20回归测试_build21_R8465_20161130
    --output=sequence
    '''
    # cmd = u'''
    # --target=com.gsafety.cloudframework:cloudframework
    # --root=E:/svn/CloudFramework/A8_resource/Mainline
    # --exclude=cloud-business-components/cloudportal-relate/portal-cms-static/portal
    # --output=sequence
    # '''

    for line in cmd.strip().splitlines():
        if line.strip() != '':
            sys.argv.append(line.strip())

# if 2 == sys.version_info[0]:
#     sys.argv = [arg.decode(sys.getfilesystemencoding()) for arg in sys.argv]

print('args : %s' % sys.argv)
# sys.argv = [arg.encode('raw_unicode_escape') for arg in sys.argv]

args = {
    'root':'.',
    'output':'sequence'
}
try:
    opts = getopt.getopt(
        sys.argv[1:],
        'r:t:i:e:o:',
        ['root=', 'target=', 'include=', 'exclude=', 'output='])[0]
except Exception:
    print('bad opts:%s' % sys.argv[1:])
    print('''
    Options:
    -r --root       : the root dir
    -t --target     : the target artifact in 'groupId:artifactId' form
    -o --output     : the output file if set
    -i --include    : which dir included, or empty for accepting all
    -e --exclude    : which dir excluded
''')
print('opts : %s' % opts)
for opt, val in opts:
    # val = val.encode('raw_unicode_escape')
    print('val [%s]' % val)

    opt = {
        '-i':'include',
        '--include':'include',
        '-e':'exclude',
        '--exclude':'exclude',
        '-r':'root',
        '--root':'root',
        '-t':'target',
        '--target':'target',
        '-o':'output',
        '--output':'output',
    }.get(opt, None)
    if opt in ('include', 'exclude'):
        args[opt] = args.get(opt, [])
        args[opt].append(val)
    elif opt in ('root', 'output', 'target'):
        args[opt] = val
print('args : %s' % args)
# map(lambda x: x.upper(), l)
def filter(abpath, relpath, isdir, name):
    if not isdir and 'pom.xml' == name:
        if 'include' in args and 0 == len([path for path in args['include'] if relpath.startswith(path)]):
            return False
        if 'exclude' in args and 0 != len([path for path in args['exclude'] if relpath.startswith(path)]):
            return False
        return True
    return False

print('collect under %s' % args['root'])
paths = FileUtils.collect(root=args['root'], filter=filter, log=False)
print('sequenceing   %s' % args['target'])
poms = MavenUtils.sequence(paths=paths, target=args['target'], log=False)



# print('writing file  %s wtih %d' % (args['output'], len(poms)))
# FileUtils.write(path=args['output'], content=json.dumps([pom.to_dict() for pom in poms], indent=4, ensure_ascii=False))

count = 0
for pom in poms:
    count += 1
    print(count)
    if not ProcessUtils.process(MavenUtils.maven(pom.path)): break