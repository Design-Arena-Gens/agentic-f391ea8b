import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import uuid
from datetime import datetime

class VectorMemory:
    def __init__(self, persist_directory: str = "./data/memory"):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory
        ))
        self.collection = self.client.get_or_create_collection(
            name="nexus_memory",
            metadata={"hnsw:space": "cosine"}
        )

    def add_memory(self, content: str, metadata: Optional[Dict] = None) -> str:
        memory_id = str(uuid.uuid4())
        if metadata is None:
            metadata = {}
        metadata["timestamp"] = datetime.utcnow().isoformat()

        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[memory_id]
        )
        return memory_id

    def query_memory(self, query: str, n_results: int = 5) -> List[Dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        memories = []
        if results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                memories.append({
                    'id': results['ids'][0][i],
                    'content': doc,
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        return memories

    def get_all_memories(self, limit: int = 100) -> List[Dict]:
        results = self.collection.get(limit=limit)
        memories = []
        for i, doc in enumerate(results['documents']):
            memories.append({
                'id': results['ids'][i],
                'content': doc,
                'metadata': results['metadatas'][i]
            })
        return memories

    def delete_memory(self, memory_id: str):
        self.collection.delete(ids=[memory_id])

    def clear_all(self):
        self.client.delete_collection("nexus_memory")
        self.collection = self.client.get_or_create_collection(
            name="nexus_memory",
            metadata={"hnsw:space": "cosine"}
        )
