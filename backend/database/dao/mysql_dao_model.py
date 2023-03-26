import mysql.connector

cnx = mysql.connector.connect(user='root',
                              password='qwertyui',
                              host='127.0.0.1',
                              database='StudyBuddy')


class DAO:
    def __init__(self, table_name, logger, cursor):
        self.table_name = table_name
        self.logger = logger
        self.cursor = cursor

    def Get(self, column, filter_by) -> str:
        query = """
            select {} 
            from {}
            where {}
        """.format(column, self.table_name, filter_by)
        self.logger.info(query)
        return query

    def GetWithPagination(self, column, filter_by, limit, offset, order_by=1) -> str:
        query = """
            SELECT {}
            FROM {}
            WHERE {}
            ORDER BY {}
            LIMIT {}, {}
        """.format(column, self.table_name, filter_by, order_by, limit, offset)
        self.logger.info(query)
        return query

    def GetLastRow(self, column) -> str:
        query = """
            SELECT {}
            FROM {}
            ORDER BY {} desc
            LIMIT 1
        """.format(column, self.table_name, column)
        self.logger.info(query)
        return query

    def Update(self, value, filter_by) -> str:
        update_value_raw = ['{} = "{}"'.format(k, v) if type(v) == str else '{} = {}'.format(k, v) for k, v in
                            value.items()]
        update_value_pair = ",".join(update_value_raw)
        query = """
            UPDATE {}
            SET {}
            WHERE {};
        """.format(self.table_name, update_value_pair, filter_by)
        self.logger.info(query)
        return query

    def Insert(self, value) -> str:
        insert_col = [k for k, v in value.items()]
        insert_val = ['"{}"'.format(v.replace("'", "\'")) if type(v) == str else "{}".format(v) for k, v in
                      value.items()]
        query = """
            INSERT INTO {}
            ({})
            VALUES ({});
        """.format(self.table_name, ",".join(insert_col), ",".join(insert_val))
        self.logger.info(query)
        return query

    def Count(self, filter_by) -> str:
        query = """
            SELECT count(1) 
            FROM {}
            WHERE {}
        """.format(self.table_name, filter_by)
        self.logger.info(query)
        return query
