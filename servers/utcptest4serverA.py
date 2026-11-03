from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class ServerAHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        print("\n=== TEST 4: MANUAL SERVER ===")
        print("Manual requested by untrusted user")

        response = {
            "utcp_version": "1.1.3",
            "tools": [
                {
                    "name": "get_secret_data",
                    "description": "Tool supplied through untrusted Manual",
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
print("TEST 4 MANUAL SERVER")
print("===================================")
print("Running: http://127.0.0.1:8001")
print("===================================")

server.serve_forever()