import requests

class Executor:

    def execute(self, request, payload):
        url = request["endpoint"]
        method = request.get("method", "POST")
        headers = request.get("headers", {})

        try:
            if method == "POST":
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=60
                )

            elif method == "GET":
                response = requests.get(
                    url,
                    params=payload,
                    headers=headers,
                    timeout=60
                )

            else:
                raise Exception("Unsupported method")

            # tenta parsear JSON
            try:
                body = response.json()
            except:
                body = response.text

            return {
                "success": True,
                "status_code": response.status_code,
                "body": body
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "timeout"
            }

        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "connection_error"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }