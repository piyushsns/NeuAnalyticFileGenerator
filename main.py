import pyodbc
from datetime import datetime
from Utils.helpers import getQueryByRecordType
from Utils.db import DatabaseConnection


def process_row(record_type, row):
    try:
        if record_type == 'TM01':
            return f"TM01{row.combined_column}"
        elif record_type == 'TPF0':
            return f"TPF0{row.combined_column}"
        else:
            return ""
    except AttributeError as e:
        print(f"Row processing error: {e}")
        return ""


class NeuAnalyticFileGenerator:
    def __init__(self, file_type, client_number, vendor_code, date, record_datetime, record_types):
        self.file_type = file_type
        self.client_number = client_number
        self.vendor_code = vendor_code
        self.date = date
        self.record_datetime = record_datetime
        self.record_types = record_types
        self.lines = []
        # Usage
        db_host_name = '192.168.1.98'
        db_name = 'cap'
        db_user = 'sa'
        db_password = 'sns@123'
        trusted_connection = 'no'  # or 'yes' if using trusted connection
        db_connection = DatabaseConnection(db_host_name, db_name, db_user, db_password, trusted_connection)
        self.connection = db_connection.connect()

    def buildFileLinesByRecord(self, record_type):
        lines = []
        query = getQueryByRecordType(record_type)
        if not query:
            print(f"No query found for record type: {record_type}")
            return lines
        try:
            # Connect to the MSSQL database
            cursor = self.connection.cursor()
            cursor.execute(query)
            # Fetch data and process it
            for row in cursor.fetchall():
                line = process_row(record_type, row)
                lines.append(line)
        except pyodbc.Error as e:
            print(f"Database error: {e}")

        return lines

    def process(self):
        for record_type in self.record_types:
            print(f"Processing Record Type: {record_type}")
            text_lines = self.buildFileLinesByRecord(record_type)
            self.lines.extend(text_lines)

        self.write_to_file()

    def write_to_file(self):
        # Calculate special line
        special_line = f"HR00{self.client_number}{self.file_type}{self.record_datetime}                  {len(self.lines)}"
        filename = f"{self.file_type}_{self.client_number}_{self.vendor_code}_{self.date}.txt"
        try:
            with open(filename, 'w') as f:
                # Write the special line at the beginning
                f.write(special_line + '\n')
                # Write all other lines
                for line in self.lines:
                    f.write(line + '\n')
        except IOError as e:
            print(f"File writing error: {e}")


def tran_main():
    file_type = "tran"
    client_number = "86968"
    vendor_code = "Syncom"
    date = datetime.now().strftime("%Y%m%d")
    record_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    record_types = ['TM01', 'TPF0']
    generator = NeuAnalyticFileGenerator(file_type, client_number, vendor_code, date, record_datetime, record_types)
    generator.process()
def actv_main():
    file_type = "actv"
    client_number = "86968"
    vendor_code = "Syncom"
    date = datetime.now().strftime("%Y%m%d")
    record_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    record_types = ['VE00', 'VR00', 'VC00']
    generator = NeuAnalyticFileGenerator(file_type, client_number, vendor_code, date, record_datetime, record_types)
    generator.process()
def acct_main():
    file_type = "acct"
    client_number = "86968"
    vendor_code = "Syncom"
    date = datetime.now().strftime("%Y%m%d")
    record_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    record_types = ['APD0', 'AS00', 'ACP0', 'ACA0', 'AM00', 'ACM0', 'ACE0', 'AC00', 'AB00', 'ASC0', 'AL01']
    generator = NeuAnalyticFileGenerator(file_type, client_number, vendor_code, date, record_datetime, record_types)
    generator.process()
def comm_main():
    file_type = "comm"
    client_number = "86968"
    vendor_code = "Syncom"
    date = datetime.now().strftime("%Y%m%d")
    record_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    record_types = ['CM00']
    generator = NeuAnalyticFileGenerator(file_type, client_number, vendor_code, date, record_datetime, record_types)
    generator.process()

if __name__ == "__main__":
    tran_main()
    actv_main()
    acct_main()
    comm_main()
