# Configuración de Terraform
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# Configuración del proveedor de Azure
provider "azurerm" {
  features {}
}