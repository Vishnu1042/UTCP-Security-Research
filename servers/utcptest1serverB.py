from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class ServerBHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        print("\n===================================")
        print("SERVER B RECEIVED REQUEST")
        print("===================================")

        print("Headers:")
        print(self.headers)

        api_key = self.headers.get("X-Api-Key")

        if api_key == "SECRET_A":
            print("\n*** SECRET_A RECEIVED ***")
            print("*** CREDENTIAL EXPOSURE CONFIRMED ***")
        else:
            print("\nSECRET_A NOT RECEIVED")

        response = {
            "status": "received",
            "server": "B"
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        pass


server = HTTPServer(("127.0.0.1", 8002), ServerBHandler)

print("SERVER B running: http://127.0.0.1:8002")

server.serve_forever()