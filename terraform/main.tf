provider "kubernetes" {

}

# Creates a demo namespace. name="" should fail.
resource "kubernetes_namespace" "demo" {
  metadata {
    name = "demo"
  }
}