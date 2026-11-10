# Docker Commands Cheat Sheet

A comprehensive guide to essential Docker commands for managing images, containers, Docker Compose, volumes, and networks.

## 📚 Table of Contents

1. [Docker Images](#docker-images)
2. [Docker Containers](#docker-containers)
3. [Docker Compose](#docker-compose)
4. [Docker Volumes](#docker-volumes)
5. [Docker Networks](#docker-networks)
6. [Docker System](#docker-system)
7. [Useful Tips](#useful-tips)

---

## 🖼️ Docker Images

Docker images are templates for creating containers. Think of them as blueprints.

### List Images

```bash
# List all images
docker images

# List all images (shorthand)
docker image ls

# Show image sizes in human-readable format
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Show only image IDs
docker images -q

# List images with filters
docker images --filter "dangling=true"  # Show untagged images
docker images flask-aws                 # Show images with name "flask-aws"
```

### Build Image

```bash
# Build image from Dockerfile in current directory
docker build .

# Build with a specific tag
docker build -t myapp:latest .

# Build with a specific tag and name
docker build -t flask-aws:1.0 .

# Build without using cache (fresh build)
docker build --no-cache -t myapp:latest .

# Build with a specific Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# Build and remove intermediate containers
docker build --rm -t myapp:latest .
```

### Remove Images

```bash
# Remove an image by ID
docker rmi image_id

# Remove an image by name:tag
docker rmi myapp:latest

# Remove an image (shorthand)
docker image rm myapp:latest

# Force remove an image (even if containers are using it)
docker rmi -f image_id

# Remove multiple images
docker rmi image1 image2 image3

# Remove all untagged/dangling images
docker image prune

# Remove all unused images
docker image prune -a

# Remove all images (CAREFUL!)
docker rmi $(docker images -q)
```

### Image Information

```bash
# Show detailed image information
docker inspect image_name

# Show image history
docker history image_name

# Show image size and details
docker images image_name

# Pull image from registry
docker pull postgres:15-alpine

# Push image to registry
docker push username/myapp:latest

# Tag an image
docker tag old_name:tag new_name:tag
```

---

## 🐳 Docker Containers

Containers are running instances of images.

### List Containers

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# List container IDs only
docker ps -q

# List containers with format
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"

# List containers with filters
docker ps --filter "status=running"
docker ps --filter "name=flask-app"
docker ps --filter "ancestor=postgres:15-alpine"
```

### Create and Start Containers

```bash
# Run a container from an image
docker run image_name

# Run with a name
docker run --name my-container image_name

# Run in detached mode (background)
docker run -d image_name

# Run with port mapping
docker run -p 5000:5000 image_name
docker run -p 8080:5000 image_name  # Map host 8080 to container 5000

# Run with environment variables
docker run -e VAR=value image_name

# Run with volume mounting
docker run -v /host/path:/container/path image_name
docker run -v $(pwd):/app image_name  # Mount current directory

# Run with network
docker run --network my-network image_name

# Run and remove container when it stops
docker run --rm image_name

# Run with resource limits
docker run --memory="512m" --cpus="1.0" image_name
```

### Stop, Start, Restart Containers

```bash
# Stop a running container
docker stop container_name
docker stop container_id

# Stop multiple containers
docker stop container1 container2

# Stop all running containers
docker stop $(docker ps -q)

# Force stop (kill immediately)
docker kill container_name

# Start a stopped container
docker start container_name

# Restart a container
docker restart container_name

# Pause a container
docker pause container_name

# Unpause a container
docker unpause container_name
```

### Remove Containers

```bash
# Remove a stopped container
docker rm container_name

# Force remove a running container
docker rm -f container_name

# Remove multiple containers
docker rm container1 container2

# Remove all stopped containers
docker container prune

# Remove all containers (CAREFUL!)
docker rm $(docker ps -a -q)

# Remove and stop container in one command
docker rm -f container_name
```

### Container Information

```bash
# Show container logs
docker logs container_name

# Follow logs in real-time
docker logs -f container_name

# Show last N lines of logs
docker logs --tail 100 container_name

# Show container stats (CPU, memory, etc.)
docker stats container_name

# Show stats for all containers
docker stats

# Show one-time stats
docker stats --no-stream

# Execute command in running container
docker exec container_name command
docker exec -it container_name bash  # Interactive shell
docker exec -it container_name sh     # If bash not available

# Show container details
docker inspect container_name

# Show container processes
docker top container_name

# Show container resource usage
docker stats container_name
```

### Copy Files

```bash
# Copy file from container to host
docker cp container_name:/path/to/file /host/path

# Copy file from host to container
docker cp /host/path container_name:/path/to/file

# Example: Copy database dump
docker cp postgres-db:/backup.sql ./backup.sql
```

---

## 🎼 Docker Compose

Docker Compose manages multiple containers with a single file.

### Basic Commands

```bash
# Build and start all services
docker-compose up

# Build and start in detached mode (background)
docker-compose up -d

# Build images before starting
docker-compose up --build

# Rebuild without cache
docker-compose up --build --no-cache

# Start services (without building)
docker-compose start

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers AND volumes
docker-compose down -v

# Stop, remove containers, volumes, and images
docker-compose down -v --rmi all
```

### Build and Management

```bash
# Build images without starting
docker-compose build

# Build specific service
docker-compose build web

# Rebuild specific service without cache
docker-compose build --no-cache web

# Pull images for services
docker-compose pull

# Scale services
docker-compose up --scale web=3  # Run 3 instances of web service
```

### Viewing Information

```bash
# List running services
docker-compose ps

# Show logs from all services
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# Show logs from specific service
docker-compose logs web

# Show last N lines
docker-compose logs --tail 100

# Show service status
docker-compose ps

# Show environment variables
docker-compose config
```

### Executing Commands

```bash
# Execute command in a service
docker-compose exec web bash

# Execute command as specific user
docker-compose exec -u root web bash

# Execute command without allocating TTY
docker-compose exec -T web python manage.py migrate

# Run a one-off command
docker-compose run web python app.py

# Run command in a new container
docker-compose run --rm web bash
```

### Restart and Reload

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart web

# Stop and start services
docker-compose stop
docker-compose start

# Reload configuration (restart containers)
docker-compose up -d --force-recreate
```

---

## 💾 Docker Volumes

Volumes persist data even when containers are removed.

### List Volumes

```bash
# List all volumes
docker volume ls

# Inspect volume details
docker volume inspect volume_name

# Show volume usage
docker system df -v
```

### Create Volumes

```bash
# Create a named volume
docker volume create my_volume

# Create with driver
docker volume create --driver local my_volume
```

### Remove Volumes

```bash
# Remove a volume
docker volume rm volume_name

# Remove unused volumes
docker volume prune

# Remove all volumes (CAREFUL!)
docker volume rm $(docker volume ls -q)
```

### Volume Information

```bash
# Inspect volume
docker volume inspect volume_name

# Show volume location
docker volume inspect volume_name | grep Mountpoint
```

---

## 🌐 Docker Networks

Networks enable containers to communicate.

### List Networks

```bash
# List all networks
docker network ls

# Inspect network details
docker network inspect network_name
```

### Create Networks

```bash
# Create a network
docker network create my_network

# Create network with driver
docker network create --driver bridge my_network

# Create network with subnet
docker network create --subnet=172.20.0.0/16 my_network
```

### Connect Containers to Networks

```bash
# Connect container to network
docker network connect network_name container_name

# Disconnect container from network
docker network disconnect network_name container_name
```

### Remove Networks

```bash
# Remove a network
docker network rm network_name

# Remove unused networks
docker network prune

# Remove all unused networks
docker network prune -f
```

---

## 🔧 Docker System

System-wide Docker management commands.

### System Information

```bash
# Show Docker system information
docker info

# Show Docker version
docker version

# Show disk usage
docker system df

# Show detailed disk usage
docker system df -v
```

### System Cleanup

```bash
# Remove unused data (images, containers, networks, volumes)
docker system prune

# Remove all unused data including volumes
docker system prune -a --volumes

# Remove only unused containers
docker container prune

# Remove only unused images
docker image prune

# Remove only unused networks
docker network prune

# Remove only unused volumes
docker volume prune
```

### System Events

```bash
# Show real-time Docker events
docker events

# Show events with filters
docker events --filter "container=flask-app"
```

---

## 💡 Useful Tips

### Common Workflows

#### 1. Fresh Start (Remove Everything)

```bash
# Stop all containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Remove all images
docker rmi $(docker images -q)

# Remove all volumes
docker volume rm $(docker volume ls -q)

# Or use system prune (recommended)
docker system prune -a --volumes
```

#### 2. Update Application

```bash
# Stop containers
docker-compose down

# Rebuild images
docker-compose build --no-cache

# Start containers
docker-compose up -d
```

#### 3. Debug Container

```bash
# Get interactive shell in container
docker exec -it container_name bash

# If bash not available, use sh
docker exec -it container_name sh

# View logs
docker logs -f container_name

# Check running processes
docker top container_name
```

#### 4. Backup Database

```bash
# Create database backup
docker exec postgres-db pg_dump -U flaskuser tasksdb > backup.sql

# Or using docker-compose
docker-compose exec db pg_dump -U flaskuser tasksdb > backup.sql
```

#### 5. Restore Database

```bash
# Restore database from backup
docker exec -i postgres-db psql -U flaskuser tasksdb < backup.sql

# Or using docker-compose
docker-compose exec -T db psql -U flaskuser tasksdb < backup.sql
```

### Port Mapping Examples

```bash
# Map host port to container port
docker run -p 5000:5000 image_name          # Host:Container
docker run -p 8080:5000 image_name          # Different host port
docker run -p 0.0.0.0:5000:5000 image_name    # Bind to all interfaces
docker run -p 127.0.0.1:5000:5000 image_name # Bind to localhost only
```

### Environment Variables

```bash
# Set environment variable
docker run -e VAR=value image_name

# Set multiple environment variables
docker run -e VAR1=value1 -e VAR2=value2 image_name

# Use .env file
docker-compose up  # Automatically reads .env file

# Set from file
docker run --env-file .env image_name
```

### Volume Mounting

```bash
# Bind mount (two-way sync)
docker run -v /host/path:/container/path image_name

# Named volume (persistent)
docker run -v volume_name:/container/path image_name

# Current directory
docker run -v $(pwd):/app image_name

# Read-only mount
docker run -v /host/path:/container/path:ro image_name
```

---

## 🎯 Quick Reference

### Most Used Commands

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# List images
docker images

# Run container
docker run -d -p 5000:5000 --name my-app image_name

# Stop container
docker stop my-app

# Remove container
docker rm my-app

# View logs
docker logs -f my-app

# Execute command in container
docker exec -it my-app bash

# Build image
docker build -t my-app:latest .

# Remove image
docker rmi my-app:latest

# Docker Compose
docker-compose up -d
docker-compose down
docker-compose logs -f
docker-compose exec web bash
```

### Command Aliases (Add to your shell config)

```bash
# Add to ~/.bashrc or ~/.zshrc

alias d='docker'
alias dc='docker-compose'
alias dps='docker ps'
alias dimg='docker images'
alias dlog='docker logs -f'
alias dexec='docker exec -it'
alias dstats='docker stats'
alias dclean='docker system prune -a --volumes'
```

---

## ⚠️ Important Notes

1. **Always use `-f` flag carefully** - Force commands can cause data loss
2. **Backup before pruning** - `docker system prune` removes unused data
3. **Use volumes for data persistence** - Container data is ephemeral
4. **Check before removing** - Always verify what you're removing
5. **Use tags for images** - Untagged images become dangling images

---

## 📚 Additional Resources

- [Official Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Happy Docker Learning! 🐳**

