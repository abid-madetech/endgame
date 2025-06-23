resource "aws_elastic_beanstalk_application" "endgame_app" {
  name = "endgame"
}

resource "aws_elastic_beanstalk_environment" "endgame_env" {
  name                = "endgame-env"
  application         = aws_elastic_beanstalk_application.endgame_app.name
  solution_stack_name = "64bit Amazon Linux 2023 v4.5.2 running Python 3.11"


  depends_on = [
    aws_iam_instance_profile.eb_instance_profile,
    aws_subnet.public_subnet,
    aws_subnet.public_subnet_2
  ]

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = aws_iam_instance_profile.eb_instance_profile.name
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DJANGO_SETTINGS_MODULE"
    value     = "config.settings"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "RDS_PASSWORD"
    value     = var.db_password
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "RDS_DB_NAME"
    value     = "postgres"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "RDS_USERNAME"
    value     = var.db_username
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "RDS_HOSTNAME"
    value     = aws_db_instance.postgres.address
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "RDS_PORT"
    value     = "5432"
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "Subnets"
    value     = join(",", [
      aws_subnet.public_subnet.id,
      aws_subnet.public_subnet_2.id
    ])
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "VPCId"
    value     = aws_vpc.main.id
  }
}
