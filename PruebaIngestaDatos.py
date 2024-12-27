import requests
import pyodbc

def test_data_ingestion():
    # Simular envío de datos a Event Hubs
    event_data = {'key': 'value'}
    response = requests.post('https://your-event-hub-url', json=event_data)
    assert response.status_code == 200

    # Verificar que los datos están en la base de datos
    server = 'your_server.database.windows.net'
    database = 'your_database'
    username = 'your_username'
    password = 'your_password'
    driver= '{ODBC Driver 17 for SQL Server}'

    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM your_table WHERE key='value'")
            row = cursor.fetchone()
            assert row is not None
