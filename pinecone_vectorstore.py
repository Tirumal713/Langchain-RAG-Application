import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class PineconeVectorStore:
    def __init__(self, api_key: str, index_name: str):
        # Initialize Pinecone client
        self.pc = Pinecone(api_key=api_key)
        self.index_name = index_name
        
        # Check if index exists, create if not
        existing_indexes = [index.name for index in self.pc.list_indexes()]
        if index_name not in existing_indexes:
            self.pc.create_index(
                name=index_name, 
                dimension=384,  # Based on sentence-transformers/all-MiniLM-L6-v2
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
        
        # Get the index
        self.index = self.pc.Index(index_name)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def embed_documents(self, documents: List[Dict[str, str]]) -> List[Dict]:
        vectors = []
        for doc in documents:
            embedding = self.embedding_model.encode(doc['text']).tolist()
            vectors.append({
                'id': f"{doc['source']}_{hash(doc['text'])}",
                'values': embedding,
                'metadata': {
                    'text': doc['text'],
                    'source': doc['source'],
                    'page': doc['page']
                }
            })
        return vectors

    def upsert_documents(self, documents: List[Dict[str, str]]):
        vectors = self.embed_documents(documents)
        self.index.upsert(vectors)

    def query(self, query: str, top_k: int = 5):
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.index.query(
            vector=query_embedding, 
            top_k=top_k, 
            include_metadata=True
        )
        return results