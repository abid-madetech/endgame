resource "aws_db_subnet_group" "public_subnet_group" {
  name       = "public-db-subnet-group"
  subnet_ids = [
    aws_subnet.public_subnet.id,
    aws_subnet.public_subnet_2.id
  ]

  tags = {
    Name = "public-db-subnet-group"
  }
}
resource "aws_db_instance" "postgres" {
  allocated_storage       = 20
  engine                  = "postgres"
  engine_version          = "15"
  instance_class          = "db.t3.micro"
  username                = var.db_username
  password                = var.db_password
  publicly_accessible     = true

  vpc_security_group_ids  = [aws_security_group.rds_public_sg.id]
  db_subnet_group_name    = aws_db_subnet_group.public_subnet_group.name

  skip_final_snapshot     = true
}
