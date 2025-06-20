variable "aws_region" {
  description = "AWS region to deploy to"
  default     = "eu-west-2"
}

variable "db_username" {
  description = "RDS master username"
  default     = "postgres"
}

variable "db_password" {
  description = "RDS master password"
  sensitive   = true
  default     = "S3curePassw0rd!"
}
