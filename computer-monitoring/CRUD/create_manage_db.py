import mysql.connector

from commons import variables
from commons.Exceptions.DBException import DBException


class ManageDB:
    """
        Needs MySQL Installed
    """

    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # move password to keyvault
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
            raise DBException("Database issue in creating the table " + str(e))

    def create_table_if_not_exists(self, table_name):
        try:
            self.cursor.execute("SHOW TABLES")
            table_names = self.cursor.fetchall()
            table_exists = False
            for table in table_names:
                table_exists = table_exists or (table_name.lower() in table)
            if not table_exists:
                self.create_table(table_name)
            self.reinitialise()
        except Exception as e:
            raise DBException("Database issue in checking or creating table exists " + str(e))

    def insert_data(self, table_name, timestamp, value):
        try:
            self.cursor.execute(variables.INSERT_TABLE_COMMAND.format(TABLE_NAME=table_name), (timestamp, value))
            self.db.commit()
            self.reinitialise()
        except Exception as e:
            raise DBException("Database issue in inserting data to the table " + str(e))
