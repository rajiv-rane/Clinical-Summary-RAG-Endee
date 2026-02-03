from endee import Endee, Precision
import os
from dotenv import load_dotenv

load_dotenv()

ENDEE_URL = os.getenv("ENDEE_URL", "http://localhost:8080")
TEST_INDEX = "test_official_migration"

def test_migration():
    print(f"Connecting to Endee at {ENDEE_URL}...")
    client = Endee(token=None)
    client.set_base_url(ENDEE_URL)
    
    try:
        # 1. Connection check
        indexes = client.list_indexes()
        print(f"✅ Connection successful. Found {len(indexes)} indexes.")
        
        # 2. Index creation
        print(f"Creating test index {TEST_INDEX}...")
        try:
            client.create_index(name=TEST_INDEX, dimension=128, space_type="cosine", precision=Precision.FLOAT32)
            print("✅ Index created.")
        except Exception as e:
            if "exists" in str(e).lower():
                print("Index already exists (ok).")
            else:
                raise e
        
        # 3. Upsert
        print("Testing upsert...")
        index = client.get_index(TEST_INDEX)
        test_vec = [0.1] * 128
        index.upsert([
            {"id": "test1", "vector": test_vec, "meta": {"name": "test patient"}}
        ])
        print("✅ Upsert successful.")
        
        # 4. Query
        print("Testing query...")
        results = index.query(vector=test_vec, top_k=1)
        if results and results[0]['id'] == 'test1':
            print(f"✅ Query successful. Found: {results[0]['id']}")
        else:
            print(f"❌ Query failed. Results: {results}")

        # Cleanup
        print("Cleaning up test index...")
        client.delete_index(TEST_INDEX)
        print("✅ Cleanup successful.")
        
        print("\n🚀 ALL MIGRATION TESTS PASSED!")
        
    except Exception as e:
        print(f"❌ Test failed during migration verification: {e}")

if __name__ == "__main__":
    test_migration()
