# -*- coding: utf-8 -*-
import os, sys, getopt

sys.path.append(os.path.dirname(__file__))

from libs import MavenUtils
from libs import FileUtils

#################################
#                               #
# Solve Maven Compile sequence  #
#                               #
#################################

sys.argv = ['DDD']

sys.argv.append('--target')
sys.argv.append('fff')
# sys.argv.append('--include')
# sys.argv.append('fff')
# sys.argv.append('-eDDD')
# sys.argv.append('-eFFF')
sys.argv.append('--root')
sys.argv.append('D:/workspace/cfw')

args = {
    'root':'.',
    'output':'sequence'
}
try:
    opts = getopt.getopt(
        sys.argv[1:],
        'r:t:i:e:',
        ['root=', 'target=', 'include=', 'exclude='])[0]
except Exception:
    print('bad opts:%s' % sys.argv[1:])
    print('''
    Options:
    -r --root       : the root dir
    -t --target     : the target artifact in 'groupId:artifactId' form
    -i --include    : which dir included, or empty for accepting all
    -e --exclude    : which dir excluded
''')
for opt, val in opts:
    opt = {
        '-i':'include',
        '--include':'include',
        '-e':'exclude',
        '--exclude':'exclude',
        '-r':'root',
        '--root':'root',
        '-t':'target',
        '--target':'target'
    }.get(opt, None)
    if opt in ('include', 'exclude'):
        args[opt] = args.get(opt, [])
        args[opt].append(val)
    elif opt in ('root', 'target'):
        args[opt] = val

# map(lambda x: x.upper(), l)
def filter(abpath, relpath, isdir, name):
    if not isdir and 'pom.xml' == name:
        if 'include' in args and 0 == len([path for path in args['include'] if relpath.startswith(path)]):
            return False
        if 'exclude' in args and 0 != len([path for path in args['exclude'] if relpath.startswith(path)]):
            return False
        return True
    return False
paths = FileUtils.collect(root=args['root'], filter=filter)
poms = MavenUtils.sequence(paths=paths, target=args[target])
FileUtils.write(file=args['output'], content='\n'.join(['%s=%s' % (pom, pom.path) for pom in poms]))