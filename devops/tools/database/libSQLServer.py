import pymssql


class Connect:
    def __init__(self, connection_info):
        self.connection_info = {
            'host': connection_info.url,
            'user': connection_info.username,
            'password': connection_info.password,
            'charset': 'utf8',
            'port': int(connection_info.port),
            'as_dict': True,
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


