output "cluster_name" {
  description = "Name of the provisioned cluster."
  value       = var.cluster_name
}

output "profile" {
  description = "Active environment profile."
  value       = var.profile
}

output "next_steps" {
  description = "What to run once the cluster is up."
  value       = <<-EOT
    1. kubectl apply -k deploy/k8s            # app + rollout + analysis
    2. kubectl apply -f deploy/argocd/        # GitOps owner
    3. Install Argo Rollouts, Prometheus, Grafana (see README)
  EOT
}
