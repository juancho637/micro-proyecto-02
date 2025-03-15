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
  dns_prefix          = "proyecto-2-k8s"

  default_node_pool {
    name                = "default"
    node_count          = var.node_min_count
    vm_size             = var.vm_size
    enable_auto_scaling = true
    min_count           = var.node_min_count
    max_count           = var.node_max_count
  }

  identity {
    type = "SystemAssigned"
  }
}