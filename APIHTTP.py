import logging
import azure.functions as func
import pyodbc
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    server = 'your_server.database.windows.net'
    database = 'your_database'
    username = 'your_username'
    password = 'your_password'
    driver= '{ODBC Driver 17 for SQL Server}'

    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM your_table")
            rows = cursor.fetchall()

    result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

    return func.HttpResponse(
        body=json.dumps(result),
        mimetype="application/json",
        status_code=200
    )
