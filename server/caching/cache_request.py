from dataclasses import dataclass, field
from typing import Any


@dataclass
class CacheRequest:
    method: str
    """The HTTP method to use for the request."""

    url: str
    """The URL to send the request to."""

    body: bytes | None = None
    """The body of the request."""

    headers: dict | None = field(default_factory=dict)
    """The headers to send with the request."""

    max_age: int = 0
    """The maximum age of the cached response in seconds."""
