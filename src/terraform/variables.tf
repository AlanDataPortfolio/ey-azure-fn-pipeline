variable "application_name" {
  description = "The name of the application"
  type        = string

}

variable "environment_name" {
  description = "The name of the environment"
  type        = string
}

variable "location" {
  description = "The Azure region to deploy to"
  type        = string
}

variable "azure_subscription_id" {
  description = "The Azure subscription ID"
  type        = string
}
