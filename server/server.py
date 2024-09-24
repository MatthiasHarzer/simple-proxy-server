from typing import Any, Literal
from fastapi.responses import PlainTextResponse
import requests
from fastapi import Body, FastAPI, HTTPException, Request, Response

from server import caching
from server.caching.cache_request import CacheRequest

ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
BODY_ALLOWED_METHODS = ["POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

cache = caching.get_cache_provider()

def sanitize_url(url: str) -> str:
    if not url.startswith("http"):
        return url

    if url.startswith("http://") or url.startswith("https://"):
        return url

    # Weird behaviour of FastAPI on linux to collapse multiple slashes
    if url.startswith("http:/") or url.startswith("https:/"):
        return url.replace("http:/", "http://").replace("https:/", "https://")

    return url

def get_url(request: Request) -> str:
    url = request.path_params.get("url", "")
    url = f"{url}?{request.query_params}" if request.query_params else url
    return sanitize_url(url)

def sanitize_headers(items: list[tuple[str, str]]) -> dict:
    sanitized_headers = {}
    for key, value in items:
        if key.lower() not in ["host", "content-length"]:
            sanitized_headers[key] = value

    return sanitized_headers

def do_proxy_request(url: str, request: Request, payload: Any | None = Body(None)) -> bytes:
    if request.method not in ALLOWED_METHODS:
        raise HTTPException(status_code=405, detail="Method Not Allowed")

    headers = sanitize_headers(request.headers.items())
    body = payload if payload and request.method in BODY_ALLOWED_METHODS else None

    try:
        proxy_request = requests.request(
            request.method, url, headers=headers, json=body)
        return proxy_request.content
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=404, detail="Connection Error")
    except:
        raise HTTPException(status_code=400, detail="Error")

def handle_proxy(request: Request, payload: Any | None = Body(None)):
    url = get_url(request)
    content = do_proxy_request(url, request, payload)
    return Response(content=content)


def handle_cache(request: Request, max_age: int, payload: Any | None = Body(None)):
    url = get_url(request)
    headers = sanitize_headers(request.headers.items())
    cache_request = CacheRequest(
        request.method,
        url,
        body=payload,
        headers=headers,
        max_age=max_age,
    )

    try:
        cached = cache.get(cache_request)
    except Exception as e:
        print(f"Error while getting from cache: {e}")
        cached = None

    if cached:
        return Response(content=cached)

    response = do_proxy_request(url, request, payload)
    try:
        cache.set(cache_request, response)
    except Exception as e:
        print(f"Error while setting cache: {e}")

    return Response(content=response)

def handle_cache_no_age(request: Request, payload: Any | None = Body(None)):
    return handle_cache(request, 0, payload)

app = FastAPI()
app.add_api_route('/cache/max-age:{max_age:int}/{url:path}', handle_cache, methods=ALLOWED_METHODS)
app.add_api_route('/cache/{url:path}', handle_cache_no_age, methods=ALLOWED_METHODS)
app.add_api_route('/{url:path}', handle_proxy, methods=ALLOWED_METHODS)
