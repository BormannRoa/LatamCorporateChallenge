# Proyecto de Ingesta, Almacenamiento y Exposición de Datos en Azure

## Descripción

Este proyecto tiene como objetivo desarrollar un sistema en la nube utilizando Azure para ingestar, almacenar y exponer datos. Se implementa mediante el uso de Infraestructura como Código (IaC) y despliegue con flujos CI/CD. Además, se incluyen pruebas de calidad, monitoreo y alertas para asegurar y monitorear la salud del sistema.

## Parte 1: Infraestructura e IaC

### 1. Identificación de la infraestructura necesaria

- **Ingesta de datos (Pub/Sub):**
  - Azure Event Hubs
  - Azure Service Bus

- **Almacenamiento de datos:**
  - Azure Synapse Analytics
  - Azure Data Lake Storage

- **Exposición de datos:**
  - Azure Functions
  - Azure API Management

### 2. Despliegue de infraestructura con Terraform

El siguiente código de ejemplo muestra cómo definir la infraestructura en Terraform:

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "East US"
}

resource "azurerm_eventhub_namespace" "example" {
  name                = "example-namespace"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  sku                 = "Standard"
}

resource "azurerm_eventhub" "example" {
  name                = "example-eventhub"
  namespace_name      = azurerm_eventhub_namespace.example.name
  resource_group_name = azurerm_resource_group.example.name
  partition_count     = 2
  message_retention   = 1
}

resource "azurerm_storage_account" "example" {
  name                     = "examplestorageacc"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_synapse_workspace" "example" {
  name                = "example-synapse"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  storage_data_lake_gen2_filesystem_id = azurerm_storage_account.example.id
  sql_administrator_login = "sqladmin"
  sql_administrator_login_password = "H@Sh1CoR3!"
}


# Parte 2: Aplicaciones y Flujo CI/CD

## Descripción

En esta parte del proyecto, se desarrollará una API HTTP para exponer datos almacenados en una base de datos y se desplegará en la nube mediante un flujo CI/CD. Además, se incluye una opción para la ingesta de datos desde un sistema Pub/Sub y un diagrama de arquitectura que muestra la interacción de los componentes.

## 1. API HTTP

### Descripción

Se levantará un endpoint HTTP que leerá datos de la base de datos y los expondrá al recibir una petición GET.

### Implementación

Usaremos Azure Functions para crear el endpoint HTTP. Aquí tienes un ejemplo básico en Python:

```python
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
# Parte 3: Pruebas de Integración y Puntos Críticos de Calidad

## Descripción

En esta parte del proyecto, se implementarán pruebas de integración para verificar que la API está exponiendo los datos correctamente, se propondrán otras pruebas de integración, se identificarán posibles puntos críticos del sistema y se propondrán formas de robustecer el sistema.

## 1. Test de Integración en el Flujo CI/CD

### Descripción

Se implementará un test de integración en el flujo CI/CD para verificar que la API efectivamente está exponiendo los datos de la base de datos.

### Implementación

**Flujo CI/CD en GitHub Actions:**

```yaml
name: Test and Deploy Azure Function

on:
  push:
    branches:
      - main

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run integration tests
      run: |
        pytest tests/integration_test.py

  deploy:
    needs: build-and-test
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Deploy to Azure Functions
      uses: Azure/functions-action@v1
      with:
        app-name: 'your-function-app-name'
        package: '.'
        publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
3. Identificar posibles puntos críticos del sistema (a nivel de fallo o performance) diferentes al punto anterior y proponer formas de testearlos o medirlos (no implementar)
Puntos Críticos:

Latencia de la Base de Datos: La latencia en las consultas a la base de datos puede afectar el rendimiento de la API.
Disponibilidad del Servicio: Fallos en Azure Event Hubs o Azure Functions pueden interrumpir el flujo de datos.
Formas de Testear o Medir:

Latencia de la Base de Datos: Usar herramientas de monitoreo como Azure Monitor para medir la latencia de las consultas y establecer alertas si superan un umbral definido.
Disponibilidad del Servicio: Implementar pruebas de disponibilidad que verifiquen periódicamente el estado de los servicios críticos y alerten en caso de fallos.
4. Proponer cómo robustecer técnicamente el sistema para compensar o solucionar dichos puntos críticos
Propuestas para Robustecer el Sistema:

Caching: Implementar un sistema de caché (por ejemplo, Azure Cache for Redis) para reducir la carga en la base de datos y mejorar la latencia de las respuestas.
Redundancia y Failover: Configurar redundancia y mecanismos de failover para Azure Event Hubs y Azure Functions para asegurar la alta disponibilidad del sistema.
Autoescalado: Configurar políticas de autoescalado en Azure para manejar incrementos en la carga de trabajo sin degradación del rendimiento.
Monitoreo y Alertas: Implementar un sistema robusto de monitoreo y alertas utilizando Azure Monitor y Application Insights para detectar y responder rápidamente a problemas de rendimiento y disponibilidad.