from typing import Any, Awaitable, Callable, Mapping, Optional

from src.Common.DatabaseManager import DatabaseManager


class CacheRepository:
    def __init__(self, mongo: DatabaseManager):
        self.mongo = mongo

    async def get_or_fetch(self, collection: str, key_field: str, key_value: Any,
                            fetch: Callable[[], Awaitable[Optional[Mapping[str, Any]]]],
                            refresh: bool = False) -> tuple[Optional[dict], bool]:
        if not refresh:
            cached = await self.mongo.find_one(collection, {key_field: key_value})
            if cached is not None:
                cached.pop('_id', None)
                return cached, True

        data = await fetch()
        if data is None:
            return None, False

        document = {**data, key_field: key_value}
        await self.mongo.upsert_one(collection, {key_field: key_value}, document)
        return document, False
