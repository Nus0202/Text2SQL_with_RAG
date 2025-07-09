import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# load schemas from JSON
# file_name = input("Please enter the schema file name (For example: schema_paragraphs.json): ")
file_name = 'schema_paragraphs.json'
with open(file_name, "r", encoding="utf-8") as f:
    paragraphs = json.load(f)
texts = [entry["content"] for entry in paragraphs]

# load FAISS index
# FAISS_name = input("Please enter the name of FAISS file name (For example: faiss_index.index): ")
FAISS_name = 'faiss_index.index'
index = faiss.read_index(FAISS_name)

# all-MiniLM-L6-v2
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_schema_paragraphs(query, top_k=3):
    query_embedding = model.encode(query, convert_to_numpy=True)
    query_embedding = np.expand_dims(query_embedding, axis=0)
    
    # FAISS: top_k
    distances, indices = index.search(query_embedding, top_k)

    # get corresponding paragraphs based on text index
    retrieved_paragraphs = [texts[i] for i in indices[0]]
    return retrieved_paragraphs