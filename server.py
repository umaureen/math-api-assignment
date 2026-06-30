from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        params = parse_qs(parsed_url.query)

        try:
            a = int(params["a"][0])
            b = int(params["b"][0])
        except:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Please provide valid numbers a and b"
            }).encode())
            return

        if path == "/add":
            result = add(a, b)
            operation = "addition"

        elif path == "/subtract":
            result = subtract(a, b)
            operation = "subtraction"

        elif path == "/multiply":
            result = multiply(a, b)
            operation = "multiplication"

        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Endpoint not found"
            }).encode())
            return

        response = {
            "a": a,
            "b": b,
            "operation": operation,
            "result": result
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


PORT = 5000

server = HTTPServer(("localhost", PORT), MyHandler)

print(f"Server running at http://localhost:{PORT}")

server.serve_forever()
