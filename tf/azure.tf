# Grupo de recursos
resource "azurerm_resource_group" "k8s" {
  name     = var.resource_group_name
  location = var.resource_group_location
}

# Cluster AKS (Azure Kubernetes Service)
resource "azurerm_kubernetes_cluster" "k8s" {
  name                = var.aks_cluster_name
  location            = azurerm_resource_group.k8s.location
  resource_group_name = azurerm_resource_group.k8s.name
  dns_prefix          = "nginx-k8s"

  default_node_pool {
    name       = "default"
    node_count = var.node_count
    vm_size    = var.vm_size
  }

  identity {
    type = "SystemAssigned"
  }
}