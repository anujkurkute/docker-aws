
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_iam_role" "ec2" {
  name = "${var.project_name}-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "ecr_read" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ec2" {
  name = "${var.project_name}-ec2-profile"
  role = aws_iam_role.ec2.name
}

resource "aws_instance" "app" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"

  subnet_id                   = aws_subnet.public["public-1"].id
  vpc_security_group_ids      = [aws_security_group.app.id]
  associate_public_ip_address = true

  iam_instance_profile = aws_iam_instance_profile.ec2.name

  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  user_data = <<-EOF
    #!/bin/bash
    set -eux

    dnf update -y
    dnf install -y docker awscli-2

    systemctl enable --now docker

    mkdir -p /opt/flask-app

    cat > /opt/flask-app/deploy.sh <<'SCRIPT'
    #!/bin/bash
    set -euo pipefail

    AWS_REGION="${var.aws_region}"
    ECR_URI="${aws_ecr_repository.app.repository_url}"
    IMAGE_TAG="$${1:-latest}"

    aws ecr get-login-password --region "$AWS_REGION" |
      docker login --username AWS --password-stdin "$ECR_URI"

    docker pull "$ECR_URI:$IMAGE_TAG"

    docker rm -f flask-app || true

    docker run -d \
      --name flask-app \
      --restart unless-stopped \
      -p 80:5000 \
      "$ECR_URI:$IMAGE_TAG"
    SCRIPT

    chmod +x /opt/flask-app/deploy.sh
  EOF

  depends_on = [
    aws_iam_role_policy_attachment.ecr_read,
    aws_iam_role_policy_attachment.ssm
  ]

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-app-server"
  })
}
