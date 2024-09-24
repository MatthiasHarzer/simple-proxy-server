from typing import Any, Literal
from fastapi.responses import PlainTextResponse
import requests
from fastapi import Body, FastAPI, Request, Response

ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]


async def handle(url: str, request: Request, payload: Any | None = Body(None)):
    if request.method not in ALLOWED_METHODS:
        return PlainTextResponse("Method Not Allowed", status_code=405)

    headers = {}
    for key, value in request.headers.items():
        if key.lower() not in ["host", "content-length"]:
            headers[key] = value
    try:
        proxy_request = requests.request(
            request.method, url, headers=headers, json=payload)
        return Response(content=proxy_request.content)
    except requests.exceptions.ConnectionError:
        return Response(content="Connection Error", status_code=404)
    except:
        return Response(content="Error", status_code=500)


app = FastAPI()
app.add_api_route('/{url:path}', handle, methods=ALLOWED_METHODS)
