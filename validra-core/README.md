# Configuring 
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Executing
uvicorn app.main:app --reload

# Testing
Open: http://127.0.0.1:8000/docs
POST /run
Click “Try it out”

{
  "endpoint": "https://jsonplaceholder.typicode.com/posts",
  "method": "POST",
  "examplePayload": {
    "title": "foo",
    "body": "bar",
    "userId": 1
  },
  "type": "fuzz"
}