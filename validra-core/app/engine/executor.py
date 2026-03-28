import requests

class Executor:

    def execute(self, request, payload, headers=None):
        url = request["endpoint"]
        method = request.get("method", "POST")
        final_headers = headers if headers is None else headers

        try:
            if method == "POST":
                response = requests.post(
                    url,
                    json=payload,
                    headers=final_headers,
                    timeout=60
                )
            elif method == "GET":
                response = requests.get(
                    url,
                    params=payload,
                    headers=final_headers,
                    timeout=60
                )
            else:
                raise Exception("Unsupported method")

            try:
                body = response.json()
            except:
                body = response.text

            return {
                "status_code": response.status_code,
                "body": body
            }

        except requests.exceptions.Timeout:
            return {
                "status_code": 408,
                "error": "timeout"
            }
        except requests.exceptions.ConnectionError:
            return {
               "status_code": 503,
                "error": "connection_error"
            }
        except Exception as e:
            return {
                "status_code": 500,
                "error": str(e)
            }