import pymysql

class Connect:
    def __init__(self, host, user, pswd, database, charset='utf8', port=3306):
        self.connection_info = {
            'host': host,
            'user': user,
            'passwd': pswd,
            'db': database,
            'charset': charset,
            'port': port,
        }

    def connection(self):
        return pymysql.connect(**self.connection_info)

    def execute(self, *sqls):
        conn = self.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        for sql in sqls:
            try:
                result = cursor.execute(sql)
            except Exception as e:
                print('-' * 64)
                print(e)
                print(sql)
                print('-' * 64)
                conn.rollback()
        result = [row for row in cursor]
        conn.commit()
        conn.close()
        return result

