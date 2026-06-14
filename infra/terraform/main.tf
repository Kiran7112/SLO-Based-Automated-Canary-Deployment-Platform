# Cluster skeleton for the SLO canary platform.
#
# Two paths are provided:
#   * profile = "local"  -> a single-node minikube cluster (default, no cloud cost)
#   * profile = "eks"    -> outline of an AWS EKS cluster for a production-grade build
#
# The local path is what you run on a laptop; the EKS block is intentionally
# left as a documented stub you flip on with `-var profile=eks`.

terraform {
  required_version = ">= 1.5"
  required_providers {
    minikube = {
      source  = "scott-the-programmer/minikube"
      version = "~> 0.4"
    }
  }
}

# --- Local profile: minikube -------------------------------------------------
provider "minikube" {}

resource "minikube_cluster" "this" {
  count        = var.profile == "local" ? 1 : 0
  cluster_name = var.cluster_name
  driver       = "docker"
  cpus         = 4
  memory       = "6000mb"
  addons       = ["ingress", "metrics-server"]
}

# --- EKS profile (stub) ------------------------------------------------------
# For a cloud build, swap in the official module. Kept commented so the local
# path applies cleanly without AWS credentials.
#
# module "eks" {
#   source          = "terraform-aws-modules/eks/aws"
#   version         = "~> 20.0"
#   cluster_name    = var.cluster_name
#   cluster_version = "1.30"
#   ...
# }
