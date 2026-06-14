variable "profile" {
  description = "Target environment: 'local' (minikube) or 'eks' (AWS)."
  type        = string
  default     = "local"

  validation {
    condition     = contains(["local", "eks"], var.profile)
    error_message = "profile must be either 'local' or 'eks'."
  }
}

variable "cluster_name" {
  description = "Name of the Kubernetes cluster."
  type        = string
  default     = "slo-canary"
}
