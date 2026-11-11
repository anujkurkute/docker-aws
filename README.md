# 8Byte DevOps Assignment

## AWS Infrastructure, CI Pipeline, Application Deployment and Monitoring

This repository contains a Flask task-management application and its
DevOps implementation on AWS. It demonstrates infrastructure
provisioning with Terraform, containerization with Docker, CI automation
with Jenkins, image storage in Amazon ECR, PostgreSQL persistence with
Amazon RDS, and monitoring and centralized logging with Amazon
CloudWatch.

> **Implementation status:** Jenkins CI, application deployment,
> CloudWatch metrics/log ingestion, and two CloudWatch dashboards were
> verified. Full automated staging-to-production deployment and HTTP
> request/error metric filters were not confirmed as completed.

## 1. Architecture

``` text
Developer
   |
 GitHub
   |
 Jenkins
   |-- Checkout
   |-- Run tests
   |-- Build Docker image
   |-- Verify image and AWS credentials
   |-- Push image
   |
 Amazon ECR
   |
 Amazon EC2 (Amazon Linux 2023)
   |
 Dockerized Flask application
   |
 Amazon RDS PostgreSQL

EC2 CloudWatch Agent ---> CloudWatch Metrics
Docker/system logs ----> CloudWatch Logs
RDS metrics -----------> CloudWatch Metrics
                           |-- 8Byte-Infrastructure-Monitoring
                           |-- 8Byte-Application-Monitoring
```

### AWS environment

  Component               Configuration
  ----------------------- ------------------------------------
  Region                  `ap-south-1` (Mumbai)
  VPC CIDR                `10.0.0.0/16`
  Network                 Two public and two private subnets
  Compute                 Amazon EC2
  OS                      Amazon Linux 2023
  Database                Amazon RDS PostgreSQL 16
  Database class          `db.t3.micro`
  Registry                Amazon ECR
  IaC                     Terraform
  CI                      Jenkins
  Monitoring/logging      Amazon CloudWatch
  Remote administration   AWS Systems Manager

RDS is configured for private access. Its security group permits
database access from the application security group.

## 2. Technology Stack

-   Python and Flask
-   PostgreSQL and SQLAlchemy
-   Docker
-   Terraform
-   Jenkins
-   Amazon ECR
-   Amazon EC2 and Amazon RDS
-   Amazon CloudWatch
-   AWS Systems Manager
-   Pytest

## 3. Repository Components

  -----------------------------------------------------------------------
  Component                           Purpose
  ----------------------------------- -----------------------------------
  `app/`                              Flask application, database
                                      integration, Docker definitions and
                                      tests

  `terraform/`                        Terraform configuration for AWS
                                      infrastructure

  `jenkins-docker/`                   Docker-related Jenkins environment
                                      configuration

  `Jenkinsfile`                       Pipeline definition, if maintained
                                      at repository root

  `docker-compose.yml`                Local development configuration, if
                                      present
  -----------------------------------------------------------------------

Adjust this overview if the final repository layout differs.

## 4. Application API

The Flask application provides task-management endpoints backed by
PostgreSQL.

  Method     Endpoint            Purpose
  ---------- ------------------- ---------------------------------
  `GET`      `/`                 Application home page
  `GET`      `/health`           Application and database health
  `GET`      `/api/tasks`        Retrieve tasks
  `POST`     `/api/tasks`        Create a task
  `PUT`      `/api/tasks/<id>`   Update a task
  `DELETE`   `/api/tasks/<id>`   Delete a task

Example health response:

``` json
{
  "database": "connected",
  "service": "flask-app",
  "status": "healthy"
}
```

Database settings are supplied through environment variables or a
database connection URL. The database initialization script creates the
schema and sample records; it should not be run on every application
startup.

## 5. Prerequisites

Install Git, Terraform, AWS CLI and Docker. Use an AWS identity with the
required permissions.

Verify AWS identity and region:

``` powershell
aws sts get-caller-identity
aws configure get region
```

The deployed resources use `ap-south-1`.

## 6. Provision Infrastructure with Terraform

``` powershell
cd terraform
terraform init
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
```

Review the plan before applying changes. Review outputs after
provisioning:

``` powershell
terraform output
```

### Terraform state and secrets

Do not commit Terraform state, plans, credentials, or local secret
files. At minimum, exclude:

``` gitignore
**/.terraform/
*.tfstate
*.tfstate.*
*.tfplan
terraform.tfvars
*.auto.tfvars
.env
.env.*
!.env.example
*.pem
*.key
```

Terraform state can contain sensitive values. For team or production
use, configure a secure remote backend and appropriate state access
controls. Do not assume a remote backend exists unless it is configured
in this project.

## 7. Build and Run with Docker

From the application directory:

``` powershell
cd app
docker build -t 8byte-devops-app .
```

Run locally with the required database environment configuration:

``` powershell
docker run -d `
  --name flask-app `
  -p 5000:5000 `
  --env-file .env `
  8byte-devops-app
```

The `.env` file is local runtime configuration and must not be
committed.

Validate the application:

``` powershell
curl.exe http://localhost:5000/health
curl.exe http://localhost:5000/api/tasks
```

## 8. Jenkins CI Pipeline

The verified Jenkins pipeline includes these stages:

1.  Checkout source from GitHub.
2.  Run application tests using the test Dockerfile.
3.  Build the Docker image.
4.  Verify the generated image.
5.  Verify AWS credentials.
6.  Authenticate to Amazon ECR.
7.  Push the image to ECR.

The image repository is:

``` text
620503470929.dkr.ecr.ap-south-1.amazonaws.com/8byte-devops-app
```

Image tag `5` was pushed during the verified run:

``` text
620503470929.dkr.ecr.ap-south-1.amazonaws.com/8byte-devops-app:5
```

**Test result:** All 5 application tests passed in the Jenkins run.

**Scope:** CI execution and image publishing were verified. Complete
automated staging-to-production deployment was not confirmed. Successful
ECR publishing should not be represented as proof of automated
production deployment.

Use Jenkins credentials or an appropriate AWS identity mechanism. Never
hardcode access keys, GitHub tokens or database passwords in pipeline
files.

## 9. Application Deployment and Validation

The Flask application runs in Docker on EC2 and connects to PostgreSQL
on RDS.

Validate the deployed application:

``` powershell
curl.exe http://<EC2-PUBLIC-IP>/health
curl.exe http://<EC2-PUBLIC-IP>/api/tasks
```

The health endpoint returned a healthy status with the database
connected. The task API returned stored task records. Replace
`<EC2-PUBLIC-IP>` with the current instance address.

## 10. CloudWatch Monitoring and Logging

The CloudWatch Agent was installed and verified as running on EC2.

### Metrics

The `CWAgent` namespace includes custom EC2 metrics such as CPU usage,
memory utilization, disk utilization, disk I/O and TCP statistics.

The `AWS/RDS` namespace provides RDS metrics such as CPU utilization,
database connections, free storage, freeable memory, network throughput,
IOPS and latency.

### Log groups

  Log group                               Purpose
  --------------------------------------- ----------------------------
  `/8byte-devops/ec2/cloud-init`          EC2 initialization logs
  `/8byte-devops/ec2/cloud-init-output`   EC2 initialization output
  `/8byte-devops/ec2/ssm-agent`           Systems Manager agent logs
  `/8byte-devops/app/docker`              Docker container logs

Retention was configured for 7 days.

### Dashboards

**`8Byte-Infrastructure-Monitoring`**

Configured with EC2 CPU, memory, disk and network metrics, plus RDS CPU,
database connections and storage metrics.

**`8Byte-Application-Monitoring`**

Configured with Docker application logs and selected EC2/RDS metrics,
including database connections, EC2 memory and CPU, and RDS freeable
memory.

### Monitoring validation

-   CloudWatch Agent status was `running` and configuration status was
    `configured`.
-   EC2 custom metrics were visible in `CWAgent`.
-   RDS metrics were available in `AWS/RDS`.
-   Docker container logs were ingested into `/8byte-devops/app/docker`.
-   Both dashboards were accepted with no dashboard validation messages
    and appeared in the dashboard list.

**Current limitation:** The observed Docker logs included Gunicorn
startup messages. HTTP request access logging and CloudWatch metric
filters for request counts and HTTP 4xx/5xx error rates were not
confirmed. Do not claim these request-level metrics are implemented.

## 11. Security

Implemented controls include:

-   RDS in private subnets.
-   RDS inbound access restricted to the application security group.
-   Security groups controlling network access.
-   Database password stored as a `SecureString` in AWS Systems Manager
    Parameter Store.
-   EC2 IAM instance role for AWS service access.
-   Systems Manager for remote administration.
-   Private Amazon ECR image repository.
-   ECR image scanning on push enabled.
-   RDS storage encryption enabled.

Use least-privilege IAM policies. Never commit AWS credentials, GitHub
tokens, database passwords, private keys or Terraform state.

## 12. Challenges and Resolutions

  -----------------------------------------------------------------------
  Challenge                           Resolution
  ----------------------------------- -----------------------------------
  AWS region access restrictions      Updated the applicable organization
                                      region allowlist.

  Application-to-database             Allowed RDS access from the
  connectivity                        application security group.

  Docker image publishing             Configured Jenkins AWS
                                      authentication and ECR permissions.

  Remote EC2 administration           Configured Systems Manager and the
                                      EC2 instance role.

  CloudWatch log collection           Installed and configured the
                                      CloudWatch Agent.

  Dashboard validation errors         Corrected metric data to the
                                      required nested array structure.

  Application validation              Checked the health endpoint and
                                      task API against the deployed
                                      application.
  -----------------------------------------------------------------------

## 13. Verification Summary

  Area                                         Status
  -------------------------------------------- ---------------------------
  Terraform infrastructure                     Provisioned
  EC2 application host                         Running
  RDS PostgreSQL                               Available
  Database connectivity                        Verified
  Docker image in ECR                          Published
  Jenkins CI pipeline                          Successful
  Application tests                            5 passed
  Health endpoint                              Healthy
  Task API                                     Verified
  CloudWatch Agent                             Running
  EC2 custom metrics                           Available
  RDS metrics                                  Available
  Docker log ingestion                         Verified
  Infrastructure dashboard                     Created
  Application dashboard                        Created
  Automated staging-to-production deployment   Not confirmed
  HTTP request/error metric filters            Not implemented/confirmed

## 14. Future Improvements

-   Add automated staging and production deployment stages.
-   Enable structured Gunicorn access logs and application request
    logging.
-   Create CloudWatch metric filters and alarms for HTTP 4xx/5xx
    responses.
-   Add alarms for CPU, memory, disk and database thresholds.
-   Add vulnerability scanning to Jenkins.
-   Implement deployment health checks and automated rollback.
-   Configure HTTPS with a valid TLS certificate.
-   Review high availability, backup and disaster recovery requirements.

## 15. Cleanup

To remove Terraform-managed resources:

``` powershell
cd terraform
terraform destroy
```

Review the destruction plan before confirming. This can interrupt the
application and delete infrastructure and data. Back up required
database data first. Resources created manually or outside Terraform may
require separate cleanup.

## 16. Conclusion

This project demonstrates an AWS DevOps workflow covering infrastructure
as code, containerization, automated testing, CI image publishing,
application/database integration, and centralized infrastructure
monitoring and logging. It provides a foundation for further
improvements in automated releases, request-level observability,
alerting and production reliability.
