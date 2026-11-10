# Docker & Docker Compose Learning Guide

This guide will teach you step-by-step how Docker and Docker Compose work by walking through this Flask full stack application.

## 📚 Table of Contents

1. [What is Docker?](#what-is-docker)
2. [What is PostgreSQL?](#what-is-postgresql)
3. [Project Structure](#project-structure)
4. [Understanding the Dockerfile](#understanding-the-dockerfile)
5. [Understanding Docker Compose](#understanding-docker-compose)
6. [Understanding PostgreSQL and Database Concepts](#understanding-postgresql-and-database-concepts)
7. [Step-by-Step: How It Works](#step-by-step-how-it-works)
8. [Common Commands](#common-commands)
9. [Key Concepts Explained](#key-concepts-explained)

---

## 🐳 What is Docker?

**Docker** is a platform that packages applications and their dependencies into lightweight containers. Think of it like a shipping container for code:

- **Traditional Way**: "It works on my machine!" - Your app might work locally but fail in production
- **Docker Way**: The container includes everything (OS, dependencies, code) - works the same everywhere!

**Key Benefits:**
- ✅ Consistency across different environments
- ✅ Isolation (apps don't interfere with each other)
- ✅ Easy deployment and scaling
- ✅ Reproducible builds

---

## 🐘 What is PostgreSQL?

**PostgreSQL** (often called "Postgres") is a powerful, open-source relational database management system (RDBMS).

### What is a Database?
A **database** is like a digital filing cabinet that stores and organizes data:
- **File Cabinet** = Database
- **Drawers** = Tables
- **Files in Drawers** = Rows (records)
- **File Labels** = Columns (fields)

### Why PostgreSQL?
- ✅ **Relational**: Data is organized in tables with relationships
- ✅ **ACID Compliant**: Guarantees data reliability (Atomicity, Consistency, Isolation, Durability)
- ✅ **Open Source**: Free and widely used
- ✅ **Robust**: Handles complex queries and large datasets
- ✅ **SQL Support**: Uses SQL (Structured Query Language) to manage data

### Key Concepts:
- **Table**: A collection of related data (e.g., "tasks" table)
- **Row**: A single record in a table (e.g., one task)
- **Column**: A field in a table (e.g., "id", "title", "completed")
- **Primary Key**: Unique identifier for each row (e.g., "id")
- **SQL**: Language to interact with the database

**In this project**: PostgreSQL stores all task data persistently, so tasks survive container restarts!

---

## 📁 Project Structure

Let's understand what each file does:

```
flask-aws/
├── app.py                    # Flask backend application (connects to PostgreSQL)
├── models.py                 # Database models (SQLAlchemy ORM)
├── database.py               # Database initialization and connection
├── requirements.txt          # Python dependencies (Flask, SQLAlchemy, PostgreSQL driver)
├── Dockerfile               # Instructions to build Docker image
├── docker-compose.yml       # Configuration for Docker Compose (web + db services)
├── .dockerignore           # Files to exclude from Docker build
├── .gitignore              # Files to exclude from Git
├── templates/              # HTML templates for Flask
│   └── index.html          # Frontend HTML page
└── static/                 # CSS, JS, images (currently empty)
```

---

## 📝 Understanding the Dockerfile

The **Dockerfile** is like a recipe that tells Docker how to build your application image.

### Line-by-Line Breakdown:

```dockerfile
FROM python:3.11-slim
```
**What it does**: Starts with a base image containing Python 3.11
- `python:3.11-slim` = Official Python image, slim version (smaller size)
- This gives you a Linux environment with Python pre-installed

**Think of it as**: Installing an operating system with Python

---

```dockerfile
WORKDIR /app
```
**What it does**: Sets `/app` as the working directory inside the container
- All subsequent commands run from this directory
- Similar to `cd /app` in a Linux terminal

---

```dockerfile
COPY requirements.txt .
```
**What it does**: Copies `requirements.txt` from your computer to the container's `/app` directory
- The `.` means current directory (which is `/app` thanks to WORKDIR)
- We copy requirements FIRST for better caching (Docker trick!)

**Why copy requirements first?**: 
- Dependencies change less often than your code
- Docker caches each step - if requirements.txt doesn't change, Docker reuses cached layers
- This makes rebuilds faster!

---

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```
**What it does**: Installs Python packages listed in requirements.txt
- `pip install` = Python package manager command
- `-r requirements.txt` = Install from requirements file
- `--no-cache-dir` = Don't store cache (keeps image smaller)

**This installs**: 
- Flask (web framework)
- SQLAlchemy (ORM - Object-Relational Mapping)
- psycopg2 (PostgreSQL driver for Python)
- Flask-SQLAlchemy (Flask integration for SQLAlchemy)

---

```dockerfile
COPY . .
```
**What it does**: Copies ALL files from your project directory to `/app` in container
- First `.` = Current directory on your machine (project root)
- Second `.` = Current directory in container (`/app`)
- `.dockerignore` file controls what gets excluded

**This copies**: `app.py`, `templates/`, `static/`, etc.

---

```dockerfile
EXPOSE 5000
```
**What it does**: Documents that the container listens on port 5000
- Doesn't actually open the port (that's done by `-p` flag or docker-compose)
- This is documentation/best practice
- Port 5000 = Flask's default port

---

```dockerfile
ENV FLASK_APP=app.py
ENV PORT=5000
```
**What it does**: Sets environment variables inside the container
- `FLASK_APP` = Tells Flask which file is the main app
- `PORT` = Port number Flask should use
- Environment variables configure the app's behavior

---

```dockerfile
CMD ["python", "app.py"]
```
**What it does**: Command that runs when container starts
- `CMD` = Default command (can be overridden)
- Runs `python app.py` to start Flask server
- This is what makes your app run!

---

## 🎯 Understanding Docker Compose

**Docker Compose** lets you define and run multiple containers with a simple YAML file.

### Why Docker Compose?
- Without Compose: You'd run `docker build` and `docker run` with many flags
- With Compose: One command (`docker-compose up`) does everything!

### Line-by-Line Breakdown:

```yaml
version: '3.8'
```
**What it does**: Specifies the Docker Compose file format version
- Different versions support different features
- `3.8` is a stable, widely-used version

---

```yaml
services:
```
**What it does**: Defines the services (containers) you want to run
- A "service" = one containerized application
- You can have multiple services (web, database, redis, etc.)

### PostgreSQL Database Service

```yaml
  db:
```
**What it does**: Names this service "db" (database)
- Other containers can connect using hostname "db"
- This is how Flask connects: `postgresql://user:pass@db:5432/dbname`

---

```yaml
    image: postgres:15-alpine
```
**What it does**: Uses pre-built PostgreSQL image instead of building from Dockerfile
- `postgres:15-alpine` = Official PostgreSQL version 15, Alpine Linux (smaller)
- No Dockerfile needed - the image is ready to use!
- Alpine = minimal Linux distribution (smaller image size)

---

```yaml
    container_name: postgres-db
```
**What it does**: Gives the PostgreSQL container a specific name
- Makes it easier to reference: `docker exec -it postgres-db psql`

---

```yaml
    environment:
      - POSTGRES_USER=flaskuser
      - POSTGRES_PASSWORD=flaskpass123
      - POSTGRES_DB=tasksdb
```
**What it does**: Sets PostgreSQL configuration
- `POSTGRES_USER` = Database username
- `POSTGRES_PASSWORD` = Database password
- `POSTGRES_DB` = Database name to create
- These environment variables initialize the database when container first starts

**Important**: These credentials must match Flask's connection string!

---

```yaml
    ports:
      - "5432:5432"
```
**What it does**: Maps PostgreSQL port 5432 to host
- Allows you to connect from your machine using database tools (like pgAdmin)
- Format: `"HOST_PORT:CONTAINER_PORT"`
- PostgreSQL default port is 5432

**Example**: Connect from host: `psql -h localhost -p 5432 -U flaskuser -d tasksdb`

---

```yaml
    volumes:
      - postgres_data:/var/lib/postgresql/data
```
**What it does**: Persists database data in a named volume
- `postgres_data` = Named volume (defined at bottom of file)
- `/var/lib/postgresql/data` = Where PostgreSQL stores data in container
- **Critical**: Without this, database data is lost when container stops!

**Why named volumes?**:
- Data survives container restarts
- Data survives `docker-compose down`
- Only lost if you explicitly remove the volume

---

```yaml
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U flaskuser -d tasksdb"]
      interval: 10s
      timeout: 5s
      retries: 5
```
**What it does**: Checks if PostgreSQL is ready to accept connections
- `pg_isready` = PostgreSQL command to check if database is ready
- `interval: 10s` = Check every 10 seconds
- `timeout: 5s` = Wait 5 seconds for response
- `retries: 5` = Try 5 times before marking as unhealthy

**Why important?**: Flask waits for database to be healthy before starting!

---

### Flask Web Service

```yaml
  web:
```
**What it does**: Names this service "web" (Flask application)

---

```yaml
    build: .
```
**What it does**: Builds Flask image from Dockerfile in current directory

---

```yaml
    depends_on:
      db:
        condition: service_healthy
```
**What it does**: Waits for database to be healthy before starting Flask
- `depends_on` = Service dependency
- `condition: service_healthy` = Wait for health check to pass
- **Ensures database is ready before Flask tries to connect!**

---

```yaml
    environment:
      - DATABASE_URL=postgresql://flaskuser:flaskpass123@db:5432/tasksdb
      - DB_HOST=db
      - DB_PORT=5432
      - DB_USER=flaskuser
      - DB_PASSWORD=flaskpass123
      - DB_NAME=tasksdb
```
**What it does**: Sets database connection information
- `DATABASE_URL` = Complete connection string (ready to use)
- Individual variables = Alternative way to construct connection string
- `DB_HOST=db` = **"db" is the service name!** Docker resolves this to the database container's IP

**Connection String Format**:
```
postgresql://username:password@host:port/database_name
```

**Key Point**: `@db:5432` uses service name "db" as hostname!
- Docker networking resolves "db" to the database container
- You don't need to know the database container's IP address
- This is why both services are on the same network!

---

```yaml
volumes:
  postgres_data:
    driver: local
```
**What it does**: Defines a named volume for database data
- `postgres_data` = Volume name (used in db service)
- `driver: local` = Store data on local machine's disk
- Creates directory: `/var/lib/docker/volumes/flask-aws_postgres_data`

**Benefits**:
- Data persists even if containers are removed
- Can be backed up
- Can be shared between containers

---

```yaml
networks:
  app-network:
    driver: bridge
```
**What it does**: Defines a Docker network
- Both `web` and `db` services are on this network
- They can communicate using service names as hostnames
- Isolated from other containers

---

## 🐘 Understanding PostgreSQL and Database Concepts

### What is SQLAlchemy ORM?

**ORM** = Object-Relational Mapping

**Without ORM** (Raw SQL):
```sql
SELECT * FROM tasks WHERE id = 1;
```

**With ORM** (SQLAlchemy):
```python
task = Task.query.get(1)
```

**Benefits**:
- Write Python code instead of SQL
- Type-safe and less error-prone
- Works with different databases (not just PostgreSQL)

### Understanding models.py

```python
class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
```

**What this creates in PostgreSQL**:

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Column Types Explained**:
- `Integer` = Whole numbers (1, 2, 3...)
- `String(200)` = Text, max 200 characters
- `Boolean` = True or False
- `DateTime` = Date and time

**Constraints Explained**:
- `primary_key=True` = Unique identifier (can't be duplicated)
- `nullable=False` = Field is required (can't be empty)
- `default=False` = Default value if not specified
- `autoincrement=True` = Automatically increases (1, 2, 3...)

### Understanding database.py

**Connection String**:
```
postgresql://username:password@host:port/database_name
postgresql://flaskuser:flaskpass123@db:5432/tasksdb
```

**Breaking it down**:
- `postgresql://` = Protocol (how to connect)
- `flaskuser:flaskpass123` = Username and password
- `@db` = Hostname (service name in docker-compose)
- `:5432` = Port number
- `/tasksdb` = Database name

**Why `@db`?**: Docker resolves service name "db" to the container's IP address automatically!

### Common Database Operations

**1. Create (INSERT)**:
```python
# SQLAlchemy
new_task = Task(title="Learn Docker", completed=False)
db.session.add(new_task)
db.session.commit()

# SQL Equivalent
INSERT INTO tasks (title, completed) VALUES ('Learn Docker', false);
```

**2. Read (SELECT)**:
```python
# SQLAlchemy
tasks = Task.query.all()  # Get all
task = Task.query.get(1)  # Get by ID

# SQL Equivalent
SELECT * FROM tasks;
SELECT * FROM tasks WHERE id = 1;
```

**3. Update (UPDATE)**:
```python
# SQLAlchemy
task = Task.query.get(1)
task.completed = True
db.session.commit()

# SQL Equivalent
UPDATE tasks SET completed = true WHERE id = 1;
```

**4. Delete (DELETE)**:
```python
# SQLAlchemy
task = Task.query.get(1)
db.session.delete(task)
db.session.commit()

# SQL Equivalent
DELETE FROM tasks WHERE id = 1;
```

### Transactions

**What is a transaction?**
A transaction groups multiple database operations together:
- Either **ALL succeed** (commit) or **ALL fail** (rollback)

**Example**:
```python
try:
    task1 = Task(title="Task 1")
    task2 = Task(title="Task 2")
    db.session.add(task1)
    db.session.add(task2)
    db.session.commit()  # Save both
except:
    db.session.rollback()  # Undo both if error
```

**Why important?**: Prevents partial data corruption!

---

## 🔄 Step-by-Step: How It Works

### When you run `docker-compose up`:

1. **Docker Compose reads `docker-compose.yml`**
   - Parses the YAML configuration
   - Identifies services: `web` and `db`

2. **Docker creates the network**
   - Creates `app-network` for services to communicate

3. **Docker starts PostgreSQL container**
   - Pulls `postgres:15-alpine` image (if not already present)
   - Creates container named `postgres-db`
   - Initializes database with username/password/database name
   - Mounts `postgres_data` volume for data persistence
   - Runs health check to verify PostgreSQL is ready

4. **Docker waits for database health check**
   - Executes `pg_isready` command
   - Waits until PostgreSQL accepts connections
   - Prevents Flask from starting before database is ready

5. **Docker builds Flask image (if needed)**
   - Looks at `build: .` → finds `Dockerfile`
   - Executes Dockerfile commands:
     - Pulls `python:3.11-slim` base image
     - Installs Python packages (Flask, SQLAlchemy, psycopg2)
     - Copies application code

6. **Docker creates and starts Flask container**
   - Creates container named `flask-app`
   - Maps port 5000:5000
   - Mounts current directory as volume (for development)
   - Sets environment variables (including DATABASE_URL)
   - Connects to `app-network` (can now reach "db" hostname)
   - Runs `CMD` command: `python app.py`

7. **Flask app initializes**
   - Reads `DATABASE_URL` from environment: `postgresql://flaskuser:flaskpass123@db:5432/tasksdb`
   - Connects to PostgreSQL database using service name "db"
   - SQLAlchemy creates tables if they don't exist (`db.create_all()`)
   - Creates sample tasks if database is empty
   - Flask listens on `0.0.0.0:5000` (all network interfaces)

8. **Application is ready!**
   - Browser → `http://localhost:5000`
   - Flask serves frontend
   - Frontend makes API requests to Flask
   - Flask queries PostgreSQL database
   - Data flows back to browser

### Request Flow (with Database):

```
Your Browser → http://localhost:5000
    ↓
Your Computer (Host) → Port 5000
    ↓
Docker Port Mapping → "5000:5000"
    ↓
Flask Container → Port 5000
    ↓
Flask App → Processes Request
    ↓
Flask → Connects to "db" hostname
    ↓
Docker Network → Resolves "db" to PostgreSQL container IP
    ↓
PostgreSQL Container → Queries Database
    ↓
Database Returns Data → Flask → Browser
```

### Database Connection Flow:

```
Flask Container (172.20.0.3)
    ↓ (Connects to "db:5432")
Docker Network Resolution
    ↓ (Resolves "db" → 172.20.0.2)
PostgreSQL Container (172.20.0.2:5432)
    ↓
PostgreSQL Database (tasksdb)
```

---

## 🛠️ Common Commands

### Building and Running:

```bash
# Build and start containers (foreground)
docker-compose up

# Build and start containers (background/detached)
docker-compose up -d

# Build images without starting
docker-compose build

# Start existing containers
docker-compose start

# Stop containers (keeps them)
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers AND volumes
docker-compose down -v
```

### Viewing Logs:

```bash
# View logs from all services
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs from specific service
docker-compose logs web
```

### Managing Containers:

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Execute command in running container
docker-compose exec web bash

# View container resource usage
docker stats
```

### Debugging:

```bash
# Check if container is running
docker-compose ps

# Restart a service
docker-compose restart web

# Rebuild without cache (fresh build)
docker-compose build --no-cache

# View detailed container info
docker inspect flask-app
```

---

## 💡 Key Concepts Explained

### 1. **Image vs Container**

- **Image** = Template/Blueprint (like a class in programming)
  - Created from Dockerfile
  - Immutable - doesn't change
  - Can create multiple containers from one image

- **Container** = Running instance of an image (like an object)
  - Created from an image
  - Can start, stop, delete
  - Changes inside container don't affect the image

**Analogy**: Image = cookie cutter, Container = actual cookie

---

### 2. **Layers in Dockerfile**

Each Dockerfile instruction creates a "layer":

```
Layer 1: FROM python:3.11-slim        (Base OS + Python)
Layer 2: WORKDIR /app                 (Directory structure)
Layer 3: COPY requirements.txt        (Dependencies file)
Layer 4: RUN pip install              (Installed packages)
Layer 5: COPY . .                     (Your code)
```

**Why layers matter**:
- Docker caches each layer
- If `requirements.txt` doesn't change, Docker reuses layers 1-3
- Only rebuilds layers 4-5
- This makes builds FASTER!

**That's why we COPY requirements.txt BEFORE copying code!**

---

### 3. **Volumes**

**Volume** = Shared directory between host and container

```yaml
volumes:
  - .:/app
```

**What happens**:
- File on your machine → Instantly available in container
- Change code → Container sees it immediately
- Perfect for development (hot reload!)

**Important**: Volumes are NOT included in the image
- Image = static snapshot
- Volume = dynamic link to your files

---

### 4. **Port Mapping**

```yaml
ports:
  - "5000:5000"
```

**Inside Container**: Flask listens on port 5000
- Container has its own network
- Port 5000 inside container ≠ Port 5000 on your machine

**Port Mapping**: Creates a bridge
- `localhost:5000` on your machine → `5000` in container
- Multiple containers can use port 5000 internally
- Only one can map to host port 5000

---

### 5. **Environment Variables**

Environment variables configure applications:

**In Dockerfile**:
```dockerfile
ENV PORT=5000
```

**In docker-compose.yml**:
```yaml
environment:
  - PORT=5000
```

**Priority**: docker-compose.yml overrides Dockerfile ENV

**Use cases**:
- Different configs for dev/production
- Database connection strings
- API keys (use secrets in production!)

---

### 6. **Networking**

Containers can communicate via networks:

```yaml
networks:
  - app-network
```

**Benefits**:
- Containers on same network can find each other
- Use service names as hostnames: `http://web:5000`
- Isolated from other containers

**Example** (with database):
```yaml
services:
  web:
    networks: [app-network]
  db:
    networks: [app-network]
# Web can connect to db using hostname "db"!
# Flask uses: postgresql://user:pass@db:5432/dbname
```

---

## 🎓 Practice Exercises

### Exercise 1: Modify the Port
1. Change the port mapping to `"8080:5000"` in `docker-compose.yml`
2. Run `docker-compose down` then `docker-compose up`
3. Access the app at `http://localhost:8080`

### Exercise 2: Add an Environment Variable
1. Add `FLASK_DEBUG=True` to docker-compose.yml environment
2. Restart the container: `docker-compose restart`
3. Check logs: `docker-compose logs -f`

### Exercise 3: Explore the Container
1. Run: `docker-compose exec web bash`
2. Inside container, try: `ls -la`, `cat app.py`, `python --version`
3. Exit with: `exit`

### Exercise 4: Rebuild from Scratch
1. Make a small change to `app.py`
2. Run: `docker-compose build --no-cache`
3. Run: `docker-compose up`
4. Watch Docker rebuild everything!

### Exercise 5: Explore PostgreSQL
1. Connect to PostgreSQL container:
   ```bash
   docker-compose exec db psql -U flaskuser -d tasksdb
   ```
2. Run SQL commands:
   ```sql
   SELECT * FROM tasks;
   \dt  -- List all tables
   \q   -- Quit
   ```
3. Verify Flask can query the database

### Exercise 6: Check Database Volume
1. Check volume exists: `docker volume ls`
2. Inspect volume: `docker volume inspect flask-aws_postgres_data`
3. See where data is stored on your machine

---

## 🚀 Next Steps

1. ✅ **Add a Database**: Already done! PostgreSQL is configured
2. **Learn SQL**: Practice writing SQL queries directly
3. **Add Redis**: Add caching layer for better performance
4. **Database Migrations**: Use Alembic for database schema versioning
5. **Multi-stage Builds**: Optimize Dockerfile for production
6. **Docker Secrets**: Securely manage API keys and passwords
7. **Backup Database**: Learn how to backup and restore PostgreSQL data

---

## 📖 Quick Reference

| Concept | Description |
|---------|-------------|
| **Image** | Blueprint/template for containers |
| **Container** | Running instance of an image |
| **Dockerfile** | Instructions to build an image |
| **docker-compose.yml** | Configuration for multiple containers |
| **Volume** | Shared directory between host and container |
| **Port Mapping** | Bridge between host and container ports |
| **Network** | Isolated communication channel for containers |
| **Volume** | Persistent storage for data (database files) |
| **Named Volume** | Docker-managed volume that survives container removal |
| **ORM** | Object-Relational Mapping (Python objects → Database tables) |
| **Transaction** | Group of database operations (all succeed or all fail) |

---

## 🐛 Common Issues

### Port Already in Use
```
Error: bind: address already in use
```
**Solution**: Change port mapping or stop the other service using port 5000

### Cannot Find Dockerfile
```
Error: Cannot locate Dockerfile
```
**Solution**: Make sure you're in the project directory with Dockerfile

### Changes Not Reflecting
**Solution**: 
- Make sure volumes are mounted: `.:/app`
- Restart container: `docker-compose restart`
- Or rebuild: `docker-compose up --build`

### Cannot Connect to Database
```
Error: connection refused
```
**Solution**: 
- Make sure database container is running: `docker-compose ps`
- Check database health: `docker-compose logs db`
- Verify connection string matches credentials
- Wait for health check to pass (Flask depends on it)

### Database Connection String Error
```
Error: invalid connection string
```
**Solution**:
- Verify format: `postgresql://user:pass@host:port/dbname`
- Make sure service name "db" matches docker-compose service name
- Check both services are on same network

### Database Data Lost
**Solution**:
- Make sure named volume is configured: `postgres_data:/var/lib/postgresql/data`
- Check volume exists: `docker volume ls`
- Data should persist unless you run `docker-compose down -v`

---

## 🎓 PostgreSQL Quick Reference

### Common SQL Commands

```sql
-- List all tables
\dt

-- Describe table structure
\d tasks

-- Select all tasks
SELECT * FROM tasks;

-- Insert a task
INSERT INTO tasks (title, completed) VALUES ('New Task', false);

-- Update a task
UPDATE tasks SET completed = true WHERE id = 1;

-- Delete a task
DELETE FROM tasks WHERE id = 1;

-- Count rows
SELECT COUNT(*) FROM tasks;

-- Exit psql
\q
```

### Connect to PostgreSQL from Host

```bash
# Using psql (if installed on your machine)
psql -h localhost -p 5432 -U flaskuser -d tasksdb

# Or via Docker
docker-compose exec db psql -U flaskuser -d tasksdb
```

---

**Happy Docker & PostgreSQL Learning! 🐳🐘**

