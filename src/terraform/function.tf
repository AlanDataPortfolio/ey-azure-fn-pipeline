resource "azurerm_storage_account" "functions" {
  name                     = "st${var.application_name}${var.environment_name}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}


resource "azurerm_service_plan" "main" {
  name                = "asp-${var.application_name}-${var.environment_name}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "Y1"
}


resource "azurerm_linux_function_app" "funcapp" {
  name                = "func-${var.application_name}-${var.environment_name}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  storage_account_name       = azurerm_storage_account.functions.name
  storage_account_access_key = azurerm_storage_account.functions.primary_access_key
  service_plan_id            = azurerm_service_plan.main.id

  site_config {
    always_on = false
    cors {
      allowed_origins     = ["https://portal.azure.com"]
      support_credentials = true
    }
    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    "APPINSIGHTS_INSTRUMENTATIONKEY" = azurerm_application_insights.main.instrumentation_key

  }

  auth_settings {
    enabled          = false
    default_provider = "Github"
  }

  identity {
    type = "SystemAssigned" #, UserAssigned
    /* identity_ids = [azurerm_user_assigned_identity.functions.id] */
  }
}


resource "azurerm_role_assignment" "storage_blob_data_contributor" {
  principal_id         = azurerm_linux_function_app.funcapp.identity[0].principal_id
  role_definition_name = "Storage Blob Data Contributor"
  scope                = azurerm_storage_account.datalake.id
}

/* resource "azurerm_user_assigned_identity" "functions" {
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  name                = "mi-${var.application_name}-${var.environment_name}-fn"
} */
