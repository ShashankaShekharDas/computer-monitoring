from datetime import datetime

import mysql.connector
from commons import variables


class ManageDB:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#####",  # move password to keyvault
            database="monitoring"
        )
        self.cursor = self.db.cursor()

    def reinitialise(self):
        self.cursor = self.db.cursor()

    def create_table(self, table_name):
        try:
            self.cursor.execute(variables.CREATE_TABLE_COMMAND.format(TABLE_NAME=table_name))
            self.reinitialise()
        except Exception as e:
            return e

    def insert_data(self, table_name, timestamp, value):
        try:
            self.cursor.execute(variables.INSERT_TABLE_COMMAND.format(TABLE_NAME=table_name), (timestamp, value))
            self.db.commit()
            self.reinitialise()
        except Exception as e:
            return e


# ManageDB().insert_data("abc", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 47.23)
