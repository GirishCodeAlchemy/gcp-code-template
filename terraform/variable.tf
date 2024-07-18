variable "project_id" {
  description = "The project ID to host the network in"
  default     = "FILL IN YOUR PROJECT ID HERE"
}

variable "network_name" {
  description = "The name of the VPC network being created"
  default     = "example-vpc"
}

variable "name" {
  description = "Name of the buckets to create."
  type        = string
  default     = "FILL IN A (UNIQUE) BUCKET NAME HERE"
}