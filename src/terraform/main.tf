resource "azurerm_resource_group" "main" {
  name     = "rg-${var.application_name}-${var.environment_name}"
  location = var.location
}

resource "random_id" "random_string" {
  byte_length = 4
}

data "azurerm_client_config" "current" {}
