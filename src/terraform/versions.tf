terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.116.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "mq-pace-2024-s2-group-data"
    storage_account_name = "sttfstate2000" # remove test
    container_name       = "tfstate2000"
    key                  = "terraform.tfstate"
    use_azuread_auth     = true
    use_oidc             = true
  }
}

provider "azurerm" {
  features {}
}
