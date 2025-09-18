from pymongo import MongoClient
from typing import List, Dict, Optional
from config.settings import Config

class MongoDBHandler:
    """MongoDB handler with connection pooling and utility methods"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self._connect()
    
    def _connect(self):
        """Establish MongoDB connection with connection pooling"""
        self.client = MongoClient(
            Config.MONGO_URI,
            maxPoolSize=50,
            waitQueueTimeoutMS=5000,
            serverSelectionTimeoutMS=5000
        )
        self.db = self.client[Config.DB_NAME]
        self.collection = self.db[Config.COLLECTION_NAME]
    
    def count_documents(self, query: Dict) -> int:
        """Count documents matching query"""
        return self.collection.count_documents(query)
    
    def find(self, query: Dict, projection: Optional[Dict] = None, limit: Optional[int] = None):
        """Find documents with optional projection and limit"""
        cursor = self.collection.find(query, projection)
        if limit:
            cursor = cursor.limit(limit)
        return cursor
    
    def bulk_write(self, operations: List, ordered: bool = False):
        """Execute bulk write operations"""
        return self.collection.bulk_write(operations, ordered=ordered)
    
    def create_index(self, index_spec: List, **kwargs):
        """Create index on collection"""
        return self.collection.create_index(index_spec, **kwargs)