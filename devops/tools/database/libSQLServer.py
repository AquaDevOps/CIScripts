import pymssql


class Connect:
    def __init__(self, host, user, password, database, charset='utf8', port=1433, as_dict=True):
        self.connection_info = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'charset': charset,
            'port': port,
            'as_dict': as_dict,
        }

    def connection(self):
        return pymssql.connect(**self.connection_info)

    def execute(self, *sqls):
        conn = self.connection()
        cursor = conn.cursor()
        for sql in sqls:
            cursor.execute(sql)
        result = [row for row in cursor]
        conn.commit()
        conn.close()
        return result


