variable "apigee_organization" {
  type = string
  description = "ID of the apigee org to deploy to."
}

variable "apigee_environment" {
  type = string
  description = "ID of the apigee environment to deploy to"
}

variable "apigee_token" {
  type = string
  description = "Apigee OAuth Access Token."
}

variable "make_api_product" {
  type = bool
  description = "Create a corresponding API Product. (Typically 'false' for namespaced deploys and utility services like the Identity Service.)"
}

variable "api_product_display_name" {
  type = string
  description = "Human-readable name for associated API Product"
  default = ""
}

variable "api_product_description" {
  type = string
  description = "Description for associated API Product"
  default = ""
}

variable "namespace" {
  type = string
  description = "Namespace to deploy proxies etc. in to, for canaries or deploys. To make it prettier, start with a hyphen (e.g. '-apm-123')."
  default = ""
}

