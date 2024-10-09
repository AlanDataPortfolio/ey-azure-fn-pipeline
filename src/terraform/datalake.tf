resource "azurerm_storage_account" "datalake" {
  name                     = "st${var.application_name}${var.environment_name}dl"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}


resource "azurerm_storage_container" "bronze" {
  name                  = "st${var.application_name}${var.environment_name}bronze"
  storage_account_name  = azurerm_storage_account.datalake.name
  container_access_type = "private"
}


resource "azurerm_storage_container" "silver" {
  name                  = "st${var.application_name}${var.environment_name}silver"
  storage_account_name  = azurerm_storage_account.datalake.name
  container_access_type = "private"
}


resource "azurerm_storage_container" "gold" {
  name                  = "st${var.application_name}${var.environment_name}gold"
  storage_account_name  = azurerm_storage_account.datalake.name
  container_access_type = "private"
}
