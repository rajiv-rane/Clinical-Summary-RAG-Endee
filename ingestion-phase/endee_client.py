
import requests
import msgpack
import json
import time
from typing import List, Dict, Any, Optional, Union

class EndeeClient:
    def __init__(self, base_url: str = "http://localhost:8080", auth_token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token
        self.headers = {}
        if self.auth_token:
            self.headers["Authorization"] = self.auth_token

    def _get_headers(self, content_type: str = "application/json") -> Dict[str, str]:
        headers = self.headers.copy()
        headers["Content-Type"] = content_type
        return headers

    def health_check(self) -> Dict[str, Any]:
        """Check if the server is running."""
        try:
            response = requests.get(f"{self.base_url}/api/v1/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"status": "error", "message": str(e)}

    def create_index(self, 
                     index_name: str, 
                     dim: int, 
                     space_type: str = "cosine", 
                     m: int = 16, 
                     ef_con: int = 200, 
                     precision: str = "float32",
                     force_recreate: bool = False) -> bool:
        """
        Create a new index.
        
        Args:
            index_name: Name of the index
            dim: Dimension of vectors
            space_type: 'l2', 'cosine', or 'ip'
            m: HNSW M parameter (default 16)
            ef_con: HNSW ef construction parameter (default 200)
            precision: 'float32', 'float16', or 'int8' (default 'float32')
            force_recreate: If True, delete existing index before creating
        """
        if force_recreate:
            self.delete_index(index_name)

        payload = {
            "index_name": index_name,
            "dim": dim,
            "space_type": space_type,
            "M": m,
            "ef_con": ef_con,
            "precision": precision
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/index/create",
                json=payload,
                headers=self._get_headers()
            )
            if response.status_code == 409: # Already exists
                print(f"Index '{index_name}' already exists.")
                return True
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error creating index: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Server response: {e.response.text}")
            return False

    def delete_index(self, index_name: str) -> bool:
        """Delete an index."""
        try:
            response = requests.delete(
                f"{self.base_url}/api/v1/index/{index_name}/delete",
                headers=self._get_headers()
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    def add_vectors(self, 
                   index_name: str, 
                   vectors: List[List[float]], 
                   ids: List[str]) -> bool:
        """
        Add vectors to the index using JSON for better reliability.
        """
        if len(vectors) != len(ids):
            raise ValueError("Number of vectors must match number of IDs")

        batch = []
        for vec, vid in zip(vectors, ids):
            batch.append({
                "id": str(vid),
                "vector": vec
            })
        
        try:
            # Endee's JSON parser handles a list of objects or a single object
            response = requests.post(
                f"{self.base_url}/api/v1/index/{index_name}/vector/insert",
                json=batch,
                headers=self._get_headers("application/json")
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error inserting vectors: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Server response: {e.response.text}")
            return False

    def search(self, 
               index_name: str, 
               query_vector: List[float], 
               k: int = 5,
               ef_search: int = 100) -> Dict[str, Any]:
        """
        Search for nearest neighbors. Endee returns results as MsgPack arrays.
        """
        payload = {
            "vector": query_vector,
            "k": k,
            "ef": ef_search,
            "include_vectors": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/index/{index_name}/search",
                json=payload,
                headers=self._get_headers()
            )
            response.raise_for_status()
            
            # Response is MsgPack: [ [similarity, id, meta, filter, norm, vector], ... ]
            if response.headers.get("Content-Type") == "application/msgpack":
                results = msgpack.unpackb(response.content, raw=False)
            else:
                results = response.json()
            
            ids = []
            similarities = []
            
            # Based on ndd::VectorResult: MSGPACK_DEFINE(similarity, id, meta, filter, norm, vector)
            if isinstance(results, list):
                for item in results:
                    if isinstance(item, list) and len(item) >= 2:
                        similarities.append(item[0])
                        ids.append(item[1])
            
            # Map back to distances (1 - similarity) for Chroma compatibility if needed
            distances = [1.0 - s for s in similarities]
            
            return {
                "ids": [ids],
                "distances": [distances],
                "documents": [[]], 
                "metadatas": [[]]
            }

        except requests.RequestException as e:
            print(f"Error searching: {e}")
            return {"ids": [], "distances": [], "documents": [], "metadatas": []}

        except requests.RequestException as e:
            print(f"Error searching: {e}")
            return {"ids": [], "distances": [], "documents": [], "metadatas": []}

