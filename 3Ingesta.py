import logging
import azure.functions as func
import pyodbc

def main(event: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s', event.get_body().decode('utf-8'))

    server = 'your_server.database.windows.net'
    database = 'your_database'
    username = 'your_username'
    password = 'your_password'
    driver= '{ODBC Driver 17 for SQL Server}'

    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO your_table (column1, column2) VALUES (?, ?)", (value1, value2))
            conn.commit()
