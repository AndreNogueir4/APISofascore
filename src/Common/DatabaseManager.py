import os
from typing import Any, Iterable, Mapping

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase
from pymongo import UpdateOne


class DatabaseManager:
    def __init__(self, uri: str = None, db_name: str = None):
        self.uri = uri or os.getenv('MONGO_URI', 'mongodb://localhost:27017')
        self.db_name = db_name or os.getenv('MONGO_DB', 'apisofascore')
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(self.uri)
        self.db: AsyncIOMotorDatabase = self.client[self.db_name]

    def collection(self, name: str) -> AsyncIOMotorCollection:
        return self.db[name]

    async def ping(self) -> bool:
        await self.client.admin.command('ping')
        return True

    async def ensure_unique_index(self, collection: str, key: str):
        await self.db[collection].create_index(key, unique=True)

    async def upsert_one(self, collection: str, query: Mapping[str, Any], data: Mapping[str, Any]):
        return await self.db[collection].update_one(query, {'$set': data}, upsert=True)

    async def upsert_many(self, collection: str, documents: Iterable[Mapping[str, Any]], key: str = '_id') -> int:
        documents = [dict(doc) for doc in documents if doc.get(key) is not None]
        if not documents:
            return 0

        operations = [UpdateOne({key: doc[key]}, {'$set': doc}, upsert=True) for doc in documents]
        result = await self.db[collection].bulk_write(operations, ordered=False)
        return result.upserted_count + result.modified_count

    async def find_all(self, collection: str, query: Mapping[str, Any] = None) -> list:
        cursor = self.db[collection].find(query or {})
        return await cursor.to_list(length=None)

    async def find_one(self, collection: str, query: Mapping[str, Any]):
        return await self.db[collection].find_one(query)

    async def close(self):
        self.client.close()

    async def __aenter__(self) -> 'DatabaseManager':
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
