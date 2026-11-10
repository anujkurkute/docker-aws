# Flask Docker Full Stack Application with PostgreSQL

A simple Flask task manager application demonstrating Docker, Docker Compose, and PostgreSQL database integration.

## 🚀 Quick Start

### Prerequisites
- Docker installed ([Get Docker](https://www.docker.com/get-started))
- Docker Compose installed (usually comes with Docker Desktop)

### Running the Application

1. **Build and start the containers:**
   ```bash
   docker-compose up
   ```
   
   Or run in detached mode (background):
   ```bash
   docker-compose up -d
   ```

2. **Access the application:**
   - Open your browser and go to: `http://localhost:5000`
   - You should see the Flask task manager interface

3. **Stop the containers:**
   ```bash
   docker-compose down
   ```

## 📚 Learning Resources

For comprehensive guides on Docker, Docker Compose, and PostgreSQL, see:
- **[docker-learn.md](./docker-learn.md)** - Complete step-by-step tutorial covering Docker, Docker Compose, and PostgreSQL
- **[DOCKER_COMMANDS.md](./DOCKER_COMMANDS.md)** - Comprehensive Docker commands cheat sheet with examples

## 🛠️ Project Structure

```
flask-aws/
├── app.py                    # Flask backend application (connects to PostgreSQL)
├── models.py                 # Database models (SQLAlchemy ORM)
├── database.py               # Database initialization and connection
├── requirements.txt          # Python dependencies (Flask, SQLAlchemy, PostgreSQL)
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Docker Compose configuration (web + db services)
├── docker-learn.md          # Comprehensive Docker & PostgreSQL tutorial
├── DOCKER_COMMANDS.md       # Docker commands cheat sheet
├── templates/               # HTML templates
│   └── index.html          # Frontend page
└── static/                 # Static files (CSS, JS)
```

## 📖 Key Commands

```bash
# Start containers
docker-compose up

# Start in background
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f

# Rebuild containers
docker-compose build

# Restart a service
docker-compose restart web
```

## 🎯 What You'll Learn

### Docker & Docker Compose:
- How Docker containers work
- How to write a Dockerfile
- How Docker Compose orchestrates containers
- Port mapping and networking
- Volumes for development and data persistence
- Environment variables

### PostgreSQL Database:
- What PostgreSQL is and how it works
- How to set up PostgreSQL in Docker
- SQLAlchemy ORM (Object-Relational Mapping)
- Database models and schema
- SQL vs Python ORM queries
- Database connections and transactions

### Integration:
- How Flask connects to PostgreSQL
- Service discovery using Docker networks
- Health checks and dependencies
- Data persistence with Docker volumes

See **[docker-learn.md](./docker-learn.md)** for detailed explanations!

## 🐘 PostgreSQL Quick Access

Connect to PostgreSQL from your machine:
```bash
docker-compose exec db psql -U flaskuser -d tasksdb
```

View database tables:
```sql
\dt
SELECT * FROM tasks;
\q
```

