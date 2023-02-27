import mysql.connector
from mysql.connector.errors import Error

database = 'studentbuddyplatform'


class DAO:
    def __init__(self, table_name, logger):
        self.table_name = table_name
        self.cnx = mysql.connector.connect(user='sbp', password='sbp',
                                           host='127.0.0.1',
                                           database=database)
        self.logger = logger

    def __del__(self):
        self.cnx.close()

    def Get(self, column, filter_by) -> (tuple, mysql.connector.Error):
        try:
            cursor = self.cnx.cursor(dictionary=True, buffered=True)
            query = """
                select {} 
                from {}
                where {}
            """.format(column, self.table_name, filter_by)
            self.logger.info(query)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result, None

        except mysql.connector.Error as err:
            return None, err.errno

    def GetWithPagination(self, column, filter_by, limit, offset, order_by=1) -> (int, tuple, mysql.connector.Error):
        try:
            cursor = self.cnx.cursor(dictionary=True, buffered=True)
            query = """
                SELECT {}
                FROM {}
                WHERE {}
                ORDER BY {}
                LIMIT {}, {}
            """.format(column, self.table_name, filter_by, order_by, limit, offset)
            self.logger.info(query)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return len(result), result, None

        except mysql.connector.Error as err:
            return 0, None, Error(errno=err.errno)

    def Update(self, value, filter_by) -> mysql.connector.Error:
        try:
            cursor = self.cnx.cursor()
            update_value_raw = ["{} = {}".format(k, v) for k, v in value.items()]
            update_value_pair = ",".join(update_value_raw)
            query = """
                UPDATE {}
                SET {}
                WHERE {};
            """.format(self.table_name, update_value_pair, filter_by)
            self.logger.info(query)
            cursor.execute(query)
            self.cnx.commit()
            return None

        except mysql.connector.Error as err:
            return Error(errno=err.errno)

    def Insert(self, value) -> mysql.connector.Error:
        try:
            cursor = self.cnx.cursor()
            insert_col = [k for k, v in value.items()]
            insert_val = [v for k, v in value.items()]
            query = """
                INSERT INTO {}
                ({})
                VALUES ({});
            """.format(self.table_name, ",".join(insert_col), ",".join(insert_val))
            self.logger.info(query)
            cursor.execute(query)
            self.cnx.commit()
            return None

        except mysql.connector.Error as err:
            return Error(errno=err.errno)

    def Count(self, filter_by) -> (int, mysql.connector.Error):
        try:
            cursor = self.cnx.cursor()
            query = """
                SELECT count(1) 
                FROM {}
                WHERE {}
            """.format(self.table_name, filter_by)
            self.logger.info(query)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result[0][0], None

        except mysql.connector.Error as err:
            return None, Error(errno=err.errno)
