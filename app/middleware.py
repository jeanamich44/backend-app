import gzip
import brotli
from starlette.types import ASGIApp, Scope, Receive, Send, Message

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
