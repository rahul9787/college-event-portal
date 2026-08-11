variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "college-event-portal"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "admin_token" {
  type      = string
  sensitive = true
}

variable "enable_lambda" {
  type    = bool
  default = false
}