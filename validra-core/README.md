# Iniciar serviços
docker compose up --build
healthy

# Acompanhar logs
docker-compose logs -f api
docker-compose logs -f ollama

# Remover containeres
docker compose down -v
docker compose restart api

docker exec -it fastapi_app sh
docker exec -it ollama sh

# To validate
USE LLM to identify responses if that is correct or not. For example null value in request returning 200, is that expected or it's a system error?