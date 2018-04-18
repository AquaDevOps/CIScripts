from . import libMySQL as mysql
try:
    from . import libSQLServer as sqlserver
except ImportError as e:
    print('sqlserver module not available')
