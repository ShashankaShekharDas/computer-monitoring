import datetime

import mysql.connector
import pyodbc

from commons import variables
from commons.Exceptions.DBException import DBException
from commons.variables import SHOW_TABLES_AZURE, AZURE_SQL_SERVER_CONNECTION_STRING


class ManageDB:
    """
        Needs MySQL Installed Locally
        and
        SQL Server in Azure
    """

    def __init__(self, enabled_azure_feeding=True, enabled_onprem_feeding=True):
        self.enabled_azure_feeding, self.enabled_onprem_feeding = enabled_azure_feeding, enabled_onprem_feeding

        if self.enabled_onprem_feeding:
            self.db_onprem = mysql.connector.connect(
                host="localhost",
                user="root",
                password="-",  # move password to keyvault
                database="monitoring"
            )
            self.cursor_onprem = self.db_onprem.cursor()

        if self.enabled_azure_feeding:
            # Initializing Azure DB
            self.db_azure = pyodbc.connect(AZURE_SQL_SERVER_CONNECTION_STRING)
            self.cursor_azure = self.db_azure.cursor()

    def reinitialise(self):
        if self.enabled_onprem_feeding:
            self.cursor_onprem = self.db_onprem.cursor()
        if self.enabled_azure_feeding:
            self.cursor_azure = self.db_azure.cursor()

    def create_table(self, table_name, for_azure=True, for_onprem=True):
        '''
            :param table_name: str
            :param for_azure: boolean Flag variable if table needs to be created for azure
            :param for_onprem: boolean Flag variable if table needs to be created for onprem
            :return:
        '''
        try:
            if self.enabled_onprem_feeding and for_onprem:
                self.cursor_onprem.execute(variables.CREATE_TABLE_COMMAND.format(TABLE_NAME=table_name))
            if self.enabled_azure_feeding and for_azure:
                self.cursor_azure.execute(variables.CREATE_TABLE_COMMAND_AZURE.format(
                    TABLE_NAME=table_name)).commit()
            self.reinitialise()
        except Exception as e:
            raise DBException("Database issue in creating the table " + str(e))

    def create_table_if_not_exists(self, table_name):
        try:
            if self.enabled_onprem_feeding:
                self.cursor_onprem.execute("SHOW TABLES")
                table_names = self.cursor_onprem.fetchall()
                table_exists = False
                for table in table_names:
                    table_exists = table_exists or (table_name.lower() in table)
                if not table_exists:
                    self.create_table(table_name, for_azure=False, for_onprem=True)
            if self.enabled_azure_feeding:
                self.cursor_azure.execute(SHOW_TABLES_AZURE)
                table_names = self.cursor_azure.fetchall()
                table_exists = False
                for table in table_names:
                    table_exists = table_exists or (table_name in table)
                if not table_exists:
                    self.create_table(table_name, for_azure=True, for_onprem=False)
            self.reinitialise()
        except Exception as e:
            raise DBException("Database issue in checking or creating table exists " + str(e))

    def insert_data(self, table_name, timestamp, value):
        try:
            if self.enabled_onprem_feeding:
                self.cursor_onprem.execute(variables.INSERT_TABLE_COMMAND.format(TABLE_NAME=table_name),
                                           (timestamp, value))
                self.db_onprem.commit()
            if self.enabled_azure_feeding:
                self.cursor_azure.execute(variables.INSERT_TABLE_COMMAND_AZURE.format(TABLE_NAME=table_name),
                                          datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                                          value)
                self.db_azure.commit()
            self.reinitialise()
        except Exception as e:
            raise DBException("Database issue in inserting data to the table " + str(e))
