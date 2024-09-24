from typing import Any, Literal
from fastapi.responses import PlainTextResponse
import requests
from fastapi import Body, FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]


def sanitize_url(url: str) -> str:
    if not url.startswith("http"):
        return url

    if url.startswith("http://") or url.startswith("https://"):
        return url

    # Weird behaviour of FastAPI on linux to collapse multiple slashes
    if url.startswith("http:/") or url.startswith("https:/"):
        return url.replace("http:/", "http://").replace("https:/", "https://")

    return url


async def handle(url: str, request: Request, payload: Any | None = Body(None)):
    if request.method not in ALLOWED_METHODS:
        return PlainTextResponse("Method Not Allowed", status_code=405)

    sanitized_url = sanitize_url(url)

    headers = {}
    for key, value in request.headers.items():
        if key.lower() not in ["host", "content-length"]:
            headers[key] = value
    try:
        proxy_request = requests.request(
            request.method, sanitized_url, headers=headers, json=payload)
        return Response(content=proxy_request.content)
    except requests.exceptions.ConnectionError:
        return Response(content="Connection Error", status_code=404)
    except:
        return Response(content="Error", status_code=500)


app = FastAPI()
app.add_api_route('/{url:path}', handle, methods=ALLOWED_METHODS)
