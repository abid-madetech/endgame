output "rds_endpoint" {
  value = aws_db_instance.postgres.endpoint
}

output "eb_url" {
  value = aws_elastic_beanstalk_environment.endgame_env.endpoint_url
}
