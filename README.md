# User API

## Description
This is a user management API built with Litestar and advanced-alchemy, providing a RESTful interface for user data with PostgreSQL as the backend database.

## Running with Docker

To run the application using Docker, follow these steps:

1. **Clone the Repository**:
    - Copy the repository to your local machine:
```bash
    git clone https://github.com/your-username/user-api.git
    cd user-api
```

2. **Configure Environment**:
- Create a `.env` file in the root directory with the following content, adjusting the values as needed:
```
    DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/user_db
```
- Ensure `alembic.ini` contains a matching `sqlalchemy.url`:
```
    [alembic]
    script_location = migrations
    sqlalchemy.url = postgresql+asyncpg://user:password@localhost:5432/user_db
```
Replace `user`, `password`, and `user_db` with the values from your `.env`.

3. **Build and Run**:
- Use the following command to build and start the application with Docker Compose:
```bash
    docker-compose up --build
```
- This will:
  - Start a PostgreSQL database container.
  - Apply database migrations automatically.
  - Launch the application on http://localhost:8000.

4. **Verify**:
- Open your browser or use a tool like `curl` to access http://localhost:8000/schema or http://localhost:8000/schema/swagger.
- Check the logs in the terminal to ensure the application and migrations started successfully.

5. **Stop the Application**:
- To stop the containers, press `Ctrl+C` or run:
```bash 
  docker-compose down
```