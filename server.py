from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import threading


PROJECT_DIR = Path(__file__).resolve().parent
LOG_PATH = PROJECT_DIR / "guestbook-log.jsonl"
MAX_REQUEST_BYTES = 4096
LOG_LOCK = threading.Lock()


class GuestbookHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/guestbook":
            entries = []
            with LOG_LOCK:
                try:
                    with LOG_PATH.open("r", encoding="utf-8") as log_file:
                        for line in log_file:
                            try:
                                entries.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue
                except FileNotFoundError:
                    pass
            self.send_json(200, list(reversed(entries[-50:])))
            return

        if self.path in ("/", "/home.html"):
            body = (PROJECT_DIR / "home.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_error(404)

    def do_POST(self):
        if self.path != "/api/guestbook":
            self.send_error(404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(400, {"error": "Invalid content length."})
            return

        if content_length < 1 or content_length > MAX_REQUEST_BYTES:
            self.send_json(413, {"error": "Request is empty or too large."})
            return

        try:
            payload = json.loads(self.rfile.read(content_length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_json(400, {"error": "Invalid JSON."})
            return

        if not isinstance(payload, dict):
            self.send_json(400, {"error": "Expected a JSON object."})
            return

        name = payload.get("name")
        message = payload.get("message")
        if not isinstance(name, str) or not isinstance(message, str):
            self.send_json(400, {"error": "Name and message must be text."})
            return

        name = name.strip()
        message = message.strip()
        if not name or len(name) > 32 or not message or len(message) > 180:
            self.send_json(400, {"error": "Name or message is empty or too long."})
            return

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "name": name,
            "message": message,
        }
        line = json.dumps(entry, ensure_ascii=False)
        with LOG_LOCK:
            with LOG_PATH.open("a", encoding="utf-8", newline="\n") as log_file:
                log_file.write(line + "\n")

        self.send_json(201, entry)

    def log_message(self, format_string, *args):
        print(f"{self.address_string()} - {format_string % args}")


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8000), GuestbookHandler)
    server.daemon_threads = True
    print("Homepage running at http://127.0.0.1:8000")
    print(f"Guestbook log: {LOG_PATH}")
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
