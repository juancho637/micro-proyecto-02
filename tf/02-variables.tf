variable "resource_group_location" {
  default     = "eastus"
  description = "Ubicación del grupo de recursos."
}

variable "resource_group_name" {
  default     = "proyecto-2-k8s-resources"
  description = "Nombre del grupo de recursos."
}

variable "aks_cluster_name" {
  default     = "proyecto-2-aks-cluster"
  description = "Nombre del cluster AKS."
}

variable "node_min_count" {
  default     = 1
  description = "Número de nodos en el cluster AKS."
}

variable "node_max_count" {
  default     = 5
  description = "Número de nodos en el cluster AKS."
}

variable "vm_size" {
  default     = "Standard_D2_v2"
  description = "Tamaño de las máquinas virtuales."
}