import os
import time
import torch
from transformers import AutoTokenizer, AutoModel
from pymongo import MongoClient
from endee import Endee, Precision
from tqdm import tqdm
from dotenv import load_dotenv

# Load env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://ishaanroopesh0102:6eShFuC0pNnFFNGm@cluster0.biujjg4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
ENDEE_URL = os.getenv("ENDEE_URL", "http://localhost:8080")
ENDEE_INDEX_NAME = os.getenv("ENDEE_INDEX_NAME", "patient_vectors")

def get_embedding_model():
    print("Loading Bio ClinicalBERT model...")
    tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
    model = AutoModel.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
    model.eval()
    if torch.cuda.is_available():
        model.to("cuda")
    print("Model loaded.")
    return tokenizer, model

def generate_embedding(text, tokenizer, model):
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
        if torch.cuda.is_available():
            inputs = {k: v.to("cuda") for k, v in inputs.items()}
        outputs = model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        emb = cls_embedding.squeeze(0)
        return emb.cpu().tolist()

def text_from_patient(patient):
    # Construct a text representation for embedding
    fields = [
        f"Chief Complaint: {patient.get('chief complaint', '')}",
        f"History: {patient.get('history of present illness', '')}",
        f"Diagnosis: {patient.get('discharge diagnosis', '')}"
    ]
    return "\n".join(fields)

def main():
    # Connect to Mongo
    client = MongoClient(MONGO_URI)
    db = client["hospital_db"]
    collection = db["test_patients"]
    
    # Connect to Endee
    endee_client = Endee(token=None)
    endee_client.set_base_url(ENDEE_URL)
    try:
        endee_client.list_indexes()
    except Exception as e:
        print(f"Cannot connect to Endee at {ENDEE_URL}: {e}")
        return

    # Create Index
    print(f"Creating/Verifying Index '{ENDEE_INDEX_NAME}'...")
    try:
        endee_client.create_index(
            name=ENDEE_INDEX_NAME, 
            dimension=768,
            space_type="cosine",
            precision=Precision.FLOAT32
        )
    except Exception as e:
        if "exists" in str(e).lower():
            print(f"Index '{ENDEE_INDEX_NAME}' already exists.")
        else:
            print(f"Error creating index: {e}")
            return
            
    # Load Model
    tokenizer, model = get_embedding_model()
    
    # Fetch patients
    patients = list(collection.find({}))
    print(f"Found {len(patients)} patients in MongoDB.")
    
    upsert_data = []
    batch_size = 50
    index = endee_client.get_index(ENDEE_INDEX_NAME)
    
    for patient in tqdm(patients):
        unit_no = str(patient.get("unit no", ""))
        if not unit_no:
            continue
            
        text = text_from_patient(patient)
        emb = generate_embedding(text, tokenizer, model)
        
        upsert_data.append({
            "id": unit_no,
            "vector": emb,
            "meta": {"unit_no": unit_no, "name": patient.get("name", "Unknown")}
        })
        
        if len(upsert_data) >= batch_size:
            try:
                index.upsert(upsert_data)
            except Exception as e:
                print(f"Failed to upload batch: {e}")
            upsert_data = []
            
    if upsert_data:
        try:
            index.upsert(upsert_data)
        except Exception as e:
            print(f"Failed to upload final batch: {e}")
        
    print("Ingestion complete!")

if __name__ == "__main__":
    main()
