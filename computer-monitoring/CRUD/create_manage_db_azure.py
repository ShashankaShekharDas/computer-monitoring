import pyodbc


class AzureSQLDriver:
    def __init__(self):
        self.connection = pyodbc.connect(
            'Driver={ODBC Driver 18 for SQL Server};Server=tcp:computermonitoring.database.windows.net,'
            '1433;Database=monitoringdb;Uid=Shashanka;Pwd=Mala_das1965;Encrypt=yes;TrustServerCertificate=no;Connection'
            'Timeout=30;')

        print("#")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE ABC(AB VARCHAR)").commit()

        # cursor = self.connection.cursor()
        # cursor.execute("SELECT * FROM TEST")
        # row = cursor.fetchone()
        # while row:
        #     print(row)
        #     row = cursor.fetchone()


AzureSQLDriver()
