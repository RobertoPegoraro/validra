import requests

class Executor:

    def execute(self, request, payload):

        url = request["endpoint"]
        method = request.get("method", "POST")

        if method == "POST":
            response = requests.post(url, json=payload)
        elif method == "GET":
            response = requests.get(url, params=payload)
        else:
            raise Exception("Unsupported method")

        return {
            "status_code": response.status_code,
            "body": response.text
        }