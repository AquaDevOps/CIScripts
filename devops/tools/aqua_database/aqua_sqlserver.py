import pymssql


class Wrapper:
    def __init__(self, connection, charset='utf8', port=1433, as_dict=True):
        self.connection_info = {
            'host': connection.host,
            'user': connection.user,
            'password': connection.pswd,
            'charset': connection.get('charset', charset),
            'port': connection.get('port', port),
            'as_dict': as_dict,
        }

    def connection(self):
        return pymssql.connect(**self.connection_info)

    def execute(self, sql):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = [row for row in cursor]
        conn.commit()
        conn.close()
        return result


