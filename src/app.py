import json
import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

INFO = {
    "app_version": os.getenv("APP_VERSION", "unknown"),
    "git_sha": os.getenv("GIT_SHA", "unknown"),
    "build_source": os.getenv("BUILD_SOURCE", "unknown"),
}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self._send(200, {"status": "ok"})
            return
        body = dict(INFO)
        body["pod"] = os.getenv("POD_NAME", socket.gethostname())
        body["node"] = os.getenv("NODE_NAME", "unknown")
        self._send(200, body)

    def _send(self, code, payload):
        data = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} {fmt % args}", flush=True)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"Listening on port {port}", flush=True)
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()