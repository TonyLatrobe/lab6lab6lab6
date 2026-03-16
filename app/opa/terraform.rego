package terraform.security

# Deny empty namespaces
deny[msg] {
  input.resource_type == "kubernetes_namespace"
  namespace := input.name
  namespace == ""
  msg := "Namespace name cannot be empty"
}