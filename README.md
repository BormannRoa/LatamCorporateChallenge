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

###Parte 4: Métricas y Monitoreo

#1. Métricas críticas

Además de las métricas básicas CPU/RAM/DISK USAGE, propongo las siguientes tres métricas críticas para entender la salud y rendimiento del sistema end-to-end:

Request latency: Tiempo promedio que tarda en procesar una solicitud desde que se recibe hasta que se devuelve la respuesta.
Error rate: Porcentaje de solicitudes que fallan y no se pueden procesar correctamente.
Data ingestion rate: Velocidad a la que se ingieren nuevos datos en el sistema, medida en términos de cantidad de datos por unidad de tiempo.
Estas métricas nos permiten entender cómo se está comportando el sistema en términos de rendimiento, estabilidad y capacidad para manejar el volumen de datos.

#2. Herramienta de visualización

La herramienta de visualización que propongo es Grafana, una plataforma de visualización de datos que nos permite crear dashboards personalizados para monitorear y analizar nuestros sistemas.

En Grafana, mostraría las siguientes métricas:

Una gráfica de línea que muestre el request latency en función del tiempo.
Un gráfico de barras que muestre el error rate en función del tiempo.
Un gráfico de área que muestre la data ingestion rate en función del tiempo.
Con esta información, podríamos entender la salud del sistema y tomar decisiones estratégicas para mejorar su rendimiento y estabilidad.

#3. Implementación en la nube

La implementación de Grafana en la nube se realizaría mediante un servicio de Azure Monitor, que nos permite recopilar y analizar métricas de nuestros sistemas en la nube. Grafana se configuraría para conectarse a Azure Monitor y recopilar las métricas críticas mencionadas anteriormente.

#4. Escalamiento a 50 sistemas similares

Si escalamos la solución a 50 sistemas similares, la visualización de Grafana cambiaría en varios aspectos:

La gráfica de línea que muestra el request latency se convertiría en una gráfica de área que muestre la media móvil del request latency en función del tiempo.
El gráfico de barras que muestra el error rate se convertiría en un gráfico de barras que muestre la media móvil del error rate en función del tiempo.
El gráfico de área que muestra la data ingestion rate se convertiría en un gráfico de área que muestre la media móvil de la data ingestion rate en función del tiempo.
Además, podríamos agregar nuevas métricas para monitorear el rendimiento y estabilidad de los 50 sistemas similares, como la media móvil del uso de recursos (CPU, RAM, DISK USAGE) y la tasa de fallos de los sistemas.

#5. Dificultades o limitaciones

Algunas dificultades o limitaciones que podrían surgir a nivel de observabilidad de los sistemas de no abordarse correctamente el problema de escalabilidad son:

La complejidad de recopilar y analizar métricas de 50 sistemas similares.
La necesidad de configurar y mantener la herramienta de visualización (Grafana) para que se adapte a los cambios en el sistema.
La posibilidad de que los sistemas no estén configurados de manera homogénea, lo que podría afectar la precisión de las métricas y la visualización.

###Parte 5: Alertas y SRE (Opcional)

1. Reglas y umbrales para alertas

Para definir reglas y umbrales para las métricas propuestas, utilizaría los siguientes umbrales:

Request latency: Si el request latency promedio supera los 500ms durante más de 5 minutos, se disparará una alerta.
Error rate: Si el error rate supera el 5% durante más de 10 minutos, se disparará una alerta.
Data ingestion rate: Si la data ingestion rate disminuye en más del 20% durante más de 30 minutos, se disparará una alerta.
Estos umbrales están basados en la experiencia y en la comprensión de los requisitos del sistema. El objetivo es detectar problemas de rendimiento y estabilidad en el sistema antes de que afecten negativamente a los usuarios.

##Argumentación

La elección de estos umbrales se basa en la comprensión de los requisitos del sistema y en la experiencia en la gestión de sistemas similares. El request latency de 500ms es un umbral razonable para considerar que el sistema está experimentando problemas de rendimiento. El error rate del 5% es un umbral razonable para considerar que el sistema está experimentando problemas de estabilidad. La data ingestion rate es un indicador importante para detectar problemas de capacidad en el sistema.

##2. Métricas SLIs y SLOs

Para definir métricas SLIs y SLOs para los servicios del sistema, utilizaría las siguientes métricas:

Service A: Request latency < 200ms, Error rate < 1%, Data ingestion rate > 1000 records/min.
Service B: Request latency < 300ms, Error rate < 2%, Data ingestion rate > 500 records/min.
Service C: Request latency < 400ms, Error rate < 3%, Data ingestion rate > 200 records/min.
Estos SLIs y SLOs están basados en la comprensión de los requisitos del sistema y en la experiencia en la gestión de sistemas similares. El objetivo es definir métricas que midan el rendimiento y estabilidad de cada servicio y que sean razonables para considerar que el servicio está funcionando correctamente.

##Argumentación

La elección de estos SLIs y SLOs se basa en la comprensión de los requisitos del sistema y en la experiencia en la gestión de sistemas similares. Los SLIs y SLOs están diseñados para medir el rendimiento y estabilidad de cada servicio y para detectar problemas de rendimiento y estabilidad en el sistema. Los umbrales están basados en la experiencia y en la comprensión de los requisitos del sistema.

## No utilizaria (Desecharia)

No utilizaría métricas como el uso de recursos (CPU, RAM, DISK USAGE) como SLIs, ya que no son indicadores directos de la performance y estabilidad del sistema. En su lugar, utilizaría métricas que midan directamente el rendimiento y estabilidad del sistema, como el request latency, error rate y data ingestion rate.