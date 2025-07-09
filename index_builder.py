import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# Step 1: Generate segments from the Markdown file
def generate_segments(md_file, json_output):
    # read Markdown
    with open(md_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    table_paragraphs = []
    current_table_lines = []

    for line in lines:
        line_stripped = line.strip()

        if line_stripped.startswith('----------------------------------------'):
            if current_table_lines:
                table_paragraphs.append("\n".join(current_table_lines).strip())
                current_table_lines = []
            continue

        if line_stripped.startswith("### Table:"):
            if current_table_lines:
                table_paragraphs.append("\n".join(current_table_lines).strip())
                current_table_lines = []
            current_table_lines.append(line_stripped)
        else:
            if current_table_lines:
                current_table_lines.append(line.rstrip())

    if current_table_lines:
        table_paragraphs.append("\n".join(current_table_lines).strip())

    output = [{"content": paragraph} for paragraph in table_paragraphs]

    with open(json_output, "w", encoding="utf-8") as f_out:
        json.dump(output, f_out, indent=4, ensure_ascii=False)

    print(f"Table paragraphs have been saved to {json_output}")

# Step 2: Compute embeddings and build a FAISS index
def vectorize_segments(json_input, faiss_output):
    # load segments from JSON
    with open(json_input, "r", encoding="utf-8") as f:
        paragraphs = json.load(f)

    # extract 'content' from JSON file
    texts = [entry["content"] for entry in paragraphs]

    # choose the embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # calculate embeddings
    embeddings = model.encode(texts, convert_to_numpy=True)

    # Build FAISS index using L2 distance
    embedding_dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embeddings)  # add embeddings to the index

    print(f"Created FAISS index with {index.ntotal} entries.")

    # Save the FAISS index to file
    faiss.write_index(index, faiss_output)
    print(f"FAISS index saved to {faiss_output}")

if __name__ == "__main__":
    md_file = input("Please enter the input markdown file name (For example: extracted_schema.md): ")          # Input Markdown file
    json_output = input("Please enter the schema json info file name (For example: schema_paragraphs.json):")    # Intermediate JSON file
    faiss_output = input("Please enter the output FAISS file name (For example: faiss_index.index): ")        # Output FAISS index file

    generate_segments(md_file, json_output)
    vectorize_segments(json_output, faiss_output)