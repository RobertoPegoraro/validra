import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"


def call_llm(prompt: str) -> dict:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3:8b-instruct-q4_0",
                "prompt": prompt,
                "stream": False, 
                "options": {
                    "temperature": 0.7,
                    "num_predict": 600,
                    "top_p": 0.9
                }
            },
            timeout=300
        )

        response.raise_for_status()

        final_text = ""

        for line in response.iter_lines():
            if not line:
                continue

            try:
                data = json.loads(line)

                # concatena resposta incremental
                if "response" in data:
                    final_text += data["response"]

                # terminou geração
                if data.get("done"):
                    break

            except json.JSONDecodeError:
                continue

        print("FINAL TEXT:", final_text)

        # tenta extrair JSON do meio do texto (mais robusto)
        return extract_json(final_text)

    except requests.exceptions.ReadTimeout:
        raise Exception("LLM timeout (model too slow or prompt too large)")

    except requests.exceptions.ConnectionError:
        raise Exception("Cannot connect to Ollama (is it running?)")

    except requests.exceptions.HTTPError as e:
        raise Exception(f"Ollama HTTP error: {e}")

    except Exception as e:
        raise Exception(f"Unexpected LLM error: {str(e)}")


def extract_json(text: str) -> dict:
    """
    Extrai JSON mesmo se vier com texto extra antes/depois
    """
    try:
        return json.loads(text)
    except:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        try:
            return json.loads(text[start:end + 1])
        except:
            pass

    raise Exception(f"Failed to parse JSON from LLM:\n{text}")