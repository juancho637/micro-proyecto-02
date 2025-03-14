output "kube_config" {
  value     = azurerm_kubernetes_cluster.k8s.kube_config_raw
  sensitive = true
  description = "Configuración de kubeconfig para conectarse al cluster"
}

output "cluster_name" {
  value = azurerm_kubernetes_cluster.k8s.name
  description = "Nombre del cluster Kubernetes"
}

output "resource_group_name" {
  value = azurerm_resource_group.k8s.name
  description = "Nombre del grupo de recursos"
}