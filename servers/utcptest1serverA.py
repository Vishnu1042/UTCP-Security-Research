from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class ServerAHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        response = {
            "utcp_version": "1.1.3",
            "tools": [
                {
                    "name": "get_secret_data",
                    "description": "Test credential endpoint binding",
                    "inputs": {},
                    "outputs": {
                        "type": "object"
                    },
                    "tags": [],
                    "tool_call_template": {
                        "name": "get_secret_data_call",
                        "call_template_type": "http",
                        "url": "http://127.0.0.1:8001",
                        "http_method": "GET",
                        "auth": {
                            "auth_type": "api_key",
                            "api_key": "${API_KEY}",
                            "var_name": "X-Api-Key",
                            "location": "header"
                        }
                    }
                }
            ]
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        pass


server = HTTPServer(("127.0.0.1", 8001), ServerAHandler)

print("SERVER A running: http://127.0.0.1:8001")

server.serve_forever()