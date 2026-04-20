import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:
    from fastapi import FastAPI, HTTPException
except Exception:
    FastAPI = None
    HTTPException = None

from backend import import_sync_payload


def _sync_payload(payload):
    try:
        return 200, import_sync_payload(payload)
    except ValueError as exc:
        return 400, {"detail": str(exc)}
    except Exception as exc:
        return 500, {"detail": f"Internal sync server error: {exc}"}


if FastAPI is not None:
    app = FastAPI(title="Pigilan Sync Server", version="1.0.0")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/sync/push")
    def sync_push(payload: dict):
        try:
            return import_sync_payload(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Internal sync server error: {exc}",
            ) from exc
else:
    app = None


class _SyncRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
            return
        self._send_json(404, {"detail": "Not found"})

    def do_POST(self):
        if self.path != "/sync/push":
            self._send_json(404, {"detail": "Not found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0

        try:
            payload_bytes = self.rfile.read(content_length) if content_length else b"{}"
            payload = json.loads(payload_bytes.decode("utf-8"))
        except Exception:
            self._send_json(400, {"detail": "Request body must be valid JSON."})
            return

        status_code, response_payload = _sync_payload(payload)
        self._send_json(status_code, response_payload)

    def log_message(self, format, *args):
        return


def run_simple_sync_server(host=None, port=None):
    server_host = host or os.environ.get("PIGILAN_SYNC_SERVER_HOST", "127.0.0.1")
    server_port = int(port or os.environ.get("PIGILAN_SYNC_SERVER_PORT", "8000"))
    server = ThreadingHTTPServer((server_host, server_port), _SyncRequestHandler)
    print(f"Pigilan sync server running at http://{server_host}:{server_port}")
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    run_simple_sync_server()
