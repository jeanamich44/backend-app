import gzip
import brotli
import hmac
import json
import os
from starlette.types import ASGIApp, Scope, Receive, Send, Message
from app.config import settings

# =====================================================================

class RequestDecompressionMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        content_encoding = headers.get(b"content-encoding", b"").decode("latin-1").lower()

        if "br" in content_encoding or "brotli" in content_encoding or "gzip" in content_encoding:
            body_parts = []
            more_body = True
            while more_body:
                message = await receive()
                body_parts.append(message.get("body", b""))
                more_body = message.get("more_body", False)

            compressed_body = b"".join(body_parts)
            try:
                if "br" in content_encoding or "brotli" in content_encoding:
                    decompressed_body = brotli.decompress(compressed_body)
                else:
                    decompressed_body = gzip.decompress(compressed_body)
            except Exception:
                decompressed_body = compressed_body

            new_headers = []
            for k, v in scope.get("headers", []):
                lower_k = k.lower()
                if lower_k == b"content-encoding" or lower_k == b"content-length":
                    continue
                new_headers.append((k, v))
            new_headers.append((b"content-length", str(len(decompressed_body)).encode("ascii")))
            scope["headers"] = new_headers

            sent = False
            async def new_receive() -> Message:
                nonlocal sent
                if not sent:
                    sent = True
                    return {
                        "type": "http.request",
                        "body": decompressed_body,
                        "more_body": False
                    }
                return {
                    "type": "http.request",
                    "body": b"",
                    "more_body": False
                }

            await self.app(scope, new_receive, send)
        else:
            await self.app(scope, receive, send)

# =====================================================================

class InternalSecretMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope.get("method", "")
        if method == "OPTIONS":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        norm_path = path.rstrip("/") or "/"
        if norm_path in ("/", "/health", "/api/payments/webhook", "/api/telegram/webhook"):
            await self.app(scope, receive, send)
            return

        expected_secret = settings.internal_api_secret or os.getenv("INTERNAL_API_SECRET", "")
        if not expected_secret:
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        incoming_secret = headers.get(b"x-internal-secret", b"").decode("latin-1").strip()

        if not hmac.compare_digest(incoming_secret, expected_secret):
            body = json.dumps({"detail": "Forbidden: invalid internal secret"}).encode("utf-8")
            response_headers = [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(body)).encode("ascii")),
            ]
            await send({
                "type": "http.response.start",
                "status": 403,
                "headers": response_headers,
            })
            await send({
                "type": "http.response.body",
                "body": body,
            })
            return

        await self.app(scope, receive, send)
