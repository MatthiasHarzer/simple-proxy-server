from server.caching.cache_provider import CacheProvider
from server.caching.cache_provider.cache_provider import TimedCache
from server.caching.cache_request import CacheRequest


class NoCacheProvider(CacheProvider):
    def _get(self, request: CacheRequest) -> TimedCache | None:
        return None

    def set(self, request: CacheRequest, response: bytes) -> None:
        pass
