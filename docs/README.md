# Nuviora Backend

This project is an API developed using FastAPI. It utilizes Docker for containerization, PostgreSQL for data storage, and Redis for caching and task queues. The project supports file processing using background tasks.

# Nuviora Backend

This project is an API developed using **FastAPI**. It utilizes Docker for containerization, PostgreSQL for data storage, and Redis for caching and task queues. The project supports file processing using background tasks and provides a scalable architecture for handling various services.

## Technology Stack
- **FastAPI** — A fast web framework for building APIs.
- **PostgreSQL** — A relational database management system for data storage.
- **Redis** — A system for caching and task queues.
- **Docker** — For application containerization.
- **Docker Compose** — For managing multi-container Docker applications.
- **Nginx** — A reverse proxy for handling HTTP requests.
- **SQLAlchemy** — An ORM for working with PostgreSQL.

## Project Structure

```plaintext
├── docker/
│   └── Dockerfile                # Dockerfile for container setup
├── nginx/
│   └── nginx.conf                # Nginx configuration
├── src/
│   ├── api/                      
│   │   └── v1/
│   │       ├── endpoints/        # API endpoint definitions
│   │       └── dependencies.py   # Dependency injection or shared dependencies
│   ├── models/                   # Database models (SQLAlchemy)
│   ├── repositories/             # Repository layer for database access
│   ├── schemas/                  # Pydantic or Marshmallow schemas for validation
│   ├── services/                 # Core business logic
│   ├── utils/                    # Utility functions
│   ├── config.py                 # Configuration settings
│   ├── database.py               # Database setup and connection management
│   └── main.py                   # Entry point for the application
├── test/                         # Unit and integration tests
├── docker-compose.yml            # Docker Compose file for multi-container setup
└── .gitignore                    # Git ignore file
```

## Installation and Running

### 1. Clone the Repository
First, clone this repository:

```bash
git clone https://github.com/nnuviora/nuviora-beckend.git
cd project-name
```

### 2. Set Up Environment Variables
Create a `.env` file and configure your environment variables as needed.

### 3. Start the Application with Docker Compose
Run the following command to build and start the containers:

Start: 
```bash
docker-compose up --build
```

Stop:
```bash
docker-compose down
```

### 4. Access the API
Once the application is running, you can access the API documentation at:

- **Swagger UI**: [http://localhost/docs](http://localhost/docs)
- **Redoc**: [http://localhost/redoc](http://localhost/redoc)
- **Website URL**: [http://yourwebsite.com](http://yourwebsite.com)

## Configuration Details

### Nginx
Nginx is used as a reverse proxy to route requests to the FastAPI application. It listens on port 80 and forwards requests to the FastAPI app running on port 8000. Static files are also served via Nginx.

To access the API through Nginx, navigate to:
- [http://localhost](http://localhost) for the main API
- [http://localhost/docs](http://localhost/docs) for Swagger UI

### Docker
Docker is used to containerize the application, ensuring a consistent environment across different systems. The FastAPI application runs inside a container, along with PostgreSQL and Redis as separate services.

### Docker Compose
Docker Compose simplifies the management of multiple containers. It defines services for the database, cache, application, and Nginx proxy, handling their dependencies and networking automatically.

## Usage
- The API provides endpoints for handling data storage, caching, and background processing.
- Use Swagger UI to test the API endpoints interactively.

## Contributing
Feel free to submit issues or pull requests if you want to contribute to the project.
