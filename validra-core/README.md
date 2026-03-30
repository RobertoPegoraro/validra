# Start Docker with FastAPI and Ollama
docker compose up --build

# Open API Doc and run
http://localhost:8000/docs


# Logs
docker-compose logs -f api ollama

# Remove/restart containers
docker compose down -v
docker compose restart api

# Exec commands
docker exec -it fastapi_app sh
docker exec -it ollama sh

# To DO
USE LLM to identify responses if that is correct or not. For example null value in request returning 200, is that expected or it's a system error?