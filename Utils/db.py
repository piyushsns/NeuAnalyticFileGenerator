import pyodbc


class DatabaseConnection:
    def __init__(self, db_host_name, db_name, db_user, db_password, trusted_connection='no'):
        self.db_host_name = db_host_name
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.trusted_connection = trusted_connection

    def connect(self):
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.db_host_name};"
            f"DATABASE={self.db_name};"
            f"UID={self.db_user};"
            f"PWD={self.db_password};"
            f"Trusted_Connection={self.trusted_connection}"
        )

        try:
            connection = pyodbc.connect(connection_string)
            print("Connection successful!")
            return connection
        except Exception as e:
            print(f"Error: {e}")
            return None


# Usage
db_host_name = '192.168.1.98'
db_name = 'cap'
db_user = 'sa'
db_password = 'sns@123'
trusted_connection = 'no'  # or 'yes' if using trusted connection

db_connection = DatabaseConnection(db_host_name, db_name, db_user, db_password, trusted_connection)
connection = db_connection.connect()

if connection:
    cursor = connection.cursor()
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    while row:
        print(row[0])
        row = cursor.fetchone()
    connection.close()
