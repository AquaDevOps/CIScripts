import pymysql


class Wrapper:
    def __init__(self, connection, charset='utf8', port=3306):
        self.connection_info = {
            'host': connection.host,
            'user': connection.user,
            'passwd': connection.pswd,
            'charset': connection.get('charset', charset),
            'port': connection.get('port', port),
        }

    def connection(self):
        return pymysql.connect(**self.connection_info)

    def execute(self, sql):
        conn = self.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql)
        except Exception as e:
            print('-' * 64)
            print(e)
            print(sql)
            print('-' * 64)
            conn.rollback()
            raise e
        result = [row for row in cursor]
        conn.commit()
        conn.close()
        return result

