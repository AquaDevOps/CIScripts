# -*- coding: utf-8 -*-
import os

# 格式化路径
def form_path(path):
    return path.replace('\\', '/')

# 采集目录下符合规范的文件(夹)
def collect(root, filter = None):
    collection = []
    # dirpath   : 文件夹路径
    # dirnames  : 文件夹下的文件夹列表
    # filenames : 文件夹下的文件列表
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            abpath = form_path(os.path.join(dirpath, filename))
            relpath = form_path(os.path.relpath(abpath, root))
            if filter is None or filter(abpath, relpath, False, filename):
                collection.append((abpath, relpath, False, filename, form_path(dirpath)))
    return collection