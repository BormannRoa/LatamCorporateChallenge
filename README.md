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
