"""
    All path are following \ instead of /, if needed modify before running
"""
PATH_TO_LIBRE_HW = r"F:\Projects\LibreHardwareMonitor-net472"
LIBRE_HW_EXECUTABLE = "LibreHardwareMonitor.exe"
CREATE_TABLE_COMMAND = "create table {TABLE_NAME}(time TIMESTAMP PRIMARY KEY,value FLOAT);"
CREATE_TABLE_COMMAND_AZURE = "create table {TABLE_NAME}(time DATETIME PRIMARY KEY,value FLOAT);"
INSERT_TABLE_COMMAND = "INSERT INTO {TABLE_NAME}(time,value) VALUES (%s,%s);"
INSERT_TABLE_COMMAND_AZURE = "INSERT INTO {TABLE_NAME}(time,value) VALUES (?,?);"
SHOW_TABLES_AZURE = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
AZURE_SQL_SERVER_CONNECTION_STRING = 'Driver={ODBC Driver 18 for SQL ' \
                                     'Server};Server=tcp:computermonitoring.database.windows.net,' \
                                     '1433;Database=monitoringdb;Uid=Shashanka;Pwd=-;Encrypt=yes' \
                                     ';TrustServerCertificate=no;Connection Timeout=30;'
