from datetime import datetime
from time import time
from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='aqua-devops',
    version='{version}.{timestamp}'.format(
        version='0.0.1', timestamp=datetime.fromtimestamp(time()).strftime('%Y%m%d.%H%M%S')
    ),
    description='lib for devops',
    packages=find_packages(),
    license='Apache 2.0',
    url='https://github.com/popingalex',
    author='popingalex',
    author_email='zhe009@hotmail.com',
    install_requires=[
        'ConfigParser >= 3.5.0',
        'PyMySQL >= 0.8.0',
        'pymssql >= 2.1.3',
        'ldap3 >= 2.4',
        'PyYAML >= 3.12',
        'pika >= 0.11.2',
        'requests >= 2.18.4',
        'selenium >= 3.11.0',
        'paramiko >= 2.4.1',
    ]
)