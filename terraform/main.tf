provider "apigee" {
  org          = var.apigee_organization
  access_token = var.apigee_token
}

terraform {
  backend "azurerm" {}

  required_providers {
    apigee = "~> 0.0"
    archive = "~> 1.3"
  }
}

module "hello-world" {
  source             = "github.com/NHSDigital/api-platform-service-module"
  name               = "hello-world"
  path               = "hello-world"
  apigee_environment = var.apigee_environment
  proxy_type         = length(regexall("sandbox", var.apigee_environment)) > 0 ? "sandbox" : "live"
  namespace          = var.namespace
  make_api_product   = true
  api_product_display_name = "Hello World Api"
  api_product_description  = "TODO: Link to docs when they are published"
}
