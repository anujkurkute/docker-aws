
output "vpc_id" {
  value = aws_vpc.main.id
}

output "rds_endpoint" {
  description = "PostgreSQL RDS endpoint"
  value       = aws_db_instance.postgres.endpoint
}

output "rds_database_name" {
  value = aws_db_instance.postgres.db_name
}

output "ecr_repository_url" {
  description = "Private ECR repository URL"
  value       = aws_ecr_repository.app.repository_url
}

output "ec2_public_ip" {
  description = "Public IP of Flask application server"
  value       = aws_instance.app.public_ip
}

output "ec2_instance_id" {
  value = aws_instance.app.id
}
