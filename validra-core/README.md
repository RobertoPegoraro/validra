# Configuration

## Create venv
python3 -m venv venv

## Activate venv and install requirements
source venv/bin/activate
pip install -r requirements.txt

# Initiate FastAPI
uvicorn app.main:app --reload

# Initiate LLM
ollama serve

# Testing
Open: http://127.0.0.1:8000/docs

Click “Try it out”


--------- Docker não finalizado

# Subir o docker para FastAPI e Ollama
docker-compose up --build

# Iniciar os serviços FastAPI e Ollama dentro do Docker
start.sh 

# Acompanhar logs
docker-compose logs -f api
docker-compose logs -f ollama