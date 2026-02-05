from endee import Endee, Precision
import os

ENDEE_URL = os.getenv("ENDEE_URL", "http://endee:8080")
INDEX_NAME = "diag_index"

def diagnose():
    client = Endee(token=None)
    client.set_base_url(ENDEE_URL)
    
    print(f"Creating diagnostic index '{INDEX_NAME}'...")
    try:
        client.create_index(name=INDEX_NAME, dimension=4, space_type="cosine", precision=Precision.FLOAT32)
    except Exception as e:
        print(f"Index creation note: {e}")
        
    index = client.get_index(INDEX_NAME)
    
    # Try Format 1: Official docs style (vector/meta)
    print("\nTesting Format 1 (vector/meta):")
    try:
        index.upsert([{"id": "v1", "vector": [0.1, 0.2, 0.3, 0.4], "meta": {"test": "data"}}])
        print("✅ Format 1 Success")
    except Exception as e:
        print(f"❌ Format 1 Failed: {e}")

    # Try Format 2: Alternative (values/metadata)
    print("\nTesting Format 2 (values/metadata):")
    try:
        index.upsert([{"id": "v2", "values": [0.1, 0.2, 0.3, 0.4], "metadata": {"test": "data"}}])
        print("✅ Format 2 Success")
    except Exception as e:
        print(f"❌ Format 2 Failed: {e}")

    # Try Format 3: Explicit parameter style
    print("\nTesting Format 3 (named parameters):")
    try:
        index.upsert(vectors=[{"id": "v3", "vector": [0.1, 0.2, 0.3, 0.4], "meta": {"test": "data"}}])
        print("✅ Format 3 Success")
    except Exception as e:
        print(f"❌ Format 3 Failed: {e}")

if __name__ == "__main__":
    diagnose()
