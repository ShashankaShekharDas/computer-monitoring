"""
    All path are following \ instead of /, if needed modify before running
"""
PATH_TO_LIBRE_HW = r"F:\Projects\LibreHardwareMonitor-net472"
LIBRE_HW_EXECUTABLE = "LibreHardwareMonitor.exe"
CREATE_TABLE_COMMAND = "create table {TABLE_NAME}(time TIMESTAMP PRIMARY KEY,value FLOAT);"
INSERT_TABLE_COMMAND = "INSERT INTO {TABLE_NAME}(time,value) VALUES (%s,%s);"
