
resource "aws_db_subnet_group" "main" {
  name       = "db-${var.project_name}-subnet-group"
  subnet_ids = [for subnet in aws_subnet.private : subnet.id]

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-db-subnet-group"
  })
}

resource "aws_db_instance" "postgres" {
  identifier = "db-${var.project_name}-postgres"

  engine         = "postgres"
  engine_version = "16"
  instance_class = "db.t3.micro"

  allocated_storage     = 20
  max_allocated_storage = 50
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = "taskdb"
  username = var.db_username
  password = var.db_password

  port                   = 5432
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  publicly_accessible = false
  multi_az            = false

  backup_retention_period    = 7
  auto_minor_version_upgrade = true

  deletion_protection = false
  skip_final_snapshot = true

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-postgres"
  })
}
