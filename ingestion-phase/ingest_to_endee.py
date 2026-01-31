
import os
import time
import torch
from transformers import AutoTokenizer, AutoModel
from pymongo import MongoClient
from endee_client import EndeeClient
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
    # Combine relevant fields
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
    endee = EndeeClient(base_url=ENDEE_URL)
    health = endee.health_check()
    if health.get("status") != "ok":
        print(f"Cannot connect to Endee at {ENDEE_URL}. Please start it first.")
        return

    # Create Index
    print(f"Creating/Verifying Index '{ENDEE_INDEX_NAME}'...")
    endee.create_index(ENDEE_INDEX_NAME, dim=768)
    
    # Load Model
    tokenizer, model = get_embedding_model()
    
    # Fetch patients
    patients = list(collection.find({}))
    print(f"Found {len(patients)} patients in MongoDB.")
    
    vectors = []
    ids = []
    
    batch_size = 50
    
    for patient in tqdm(patients):
        unit_no = str(patient.get("unit no", ""))
        if not unit_no:
            continue
            
        text = text_from_patient(patient)
        emb = generate_embedding(text, tokenizer, model)
        
        vectors.append(emb)
        ids.append(unit_no)
        
        if len(vectors) >= batch_size:
            success = endee.add_vectors(ENDEE_INDEX_NAME, vectors, ids)
            if not success:
                print("Failed to upload batch")
            vectors = []
            ids = []
            
    if vectors:
        endee.add_vectors(ENDEE_INDEX_NAME, vectors, ids)
        
    print("Ingestion complete!")

if __name__ == "__main__":
    main()
