import os
import sys


class Node:
    def __init__(self, abspath, relpath, dirpath, name, ext):
        self.abspath = abspath
        self.relpath = relpath
        self.dirpath = dirpath
        self.name = name
        self.ext = ext


def form_path(path):
    return path.replace('\\', '/')


def collect(root, accept=lambda **x: True, log=False):
    # dirpath   : 文件夹路径
    # dirnames  : 文件夹下的文件夹列表
    # filenames : 文件夹下的文件列表
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            abspath = form_path(os.path.join(dirpath, filename))
            relpath = form_path(os.path.relpath(abspath, root))
            splitext = os.path.splitext(filename)
            if accept(abspath=abspath, relpath=relpath, isdir=False, filename=filename):
                if log:
                    print('accepting : %s' % abspath)
                yield Node(
                    abspath=abspath,
                    relpath=relpath,
                    dirpath=form_path(dirpath),
                    name=splitext[0],
                    ext=splitext[1],
                )
