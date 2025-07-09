# 🧠 Text2SQL with Retrieval-Augmented Generation (RAG)

A modular, locally-deployable **Text-to-SQL** system integrating **Retrieval-Augmented Generation (RAG)** with **Large Language Models (LLMs)** to convert natural language questions into executable SQL queries—without fine-tuning.

> **Authors:** Zhengxiao Sun
> **Course:** CIS6400 — Machine Learning for Sequences  
> **Institution:** University of Guelph, Canada  
> **Date:** July 2025

---

## 🚀 Project Overview

This project explores how combining Retrieval-Augmented Generation (RAG) with LLMs can improve **zero-shot** Text-to-SQL performance. The system transforms user questions into SQL queries grounded in relevant schema segments—retrieved dynamically using vector embeddings—thereby avoiding hallucinations and improving accuracy for complex SQL tasks.

---

## 🧩 Key Features

- 🧾 **Zero-shot SQL generation** without fine-tuning
- 🔍 **Semantic retrieval** using FAISS and SentenceTransformers
- 📦 **Local inference** with Deepseek-8B model via Ollama
- 🔧 **Modular pipeline**: preprocessing → embedding → retrieval → prompt → generation
- 📊 **Manual evaluation** on 100 curated Spider-based examples

---

## 🏗️ System Architecture

### 🔄 Pipeline Steps

1. **User Query Input** – Accept natural language query.
2. **Schema Embedding & Indexing** – Encode schema using `MiniLM` and index with FAISS.
3. **Top-k Schema Retrieval** – Retrieve most relevant schema chunks.
4. **Prompt Construction** – Combine schema and query into structured prompt.
5. **LLM Inference** – Generate SQL using `Deepseek-r1:8B` locally.
6. **Evaluation** – Manual comparison with ground-truth SQL for correctness.

### 📌 System Design Highlights

- **No cloud APIs** required: fully local and privacy-friendly.
- **Easy to extend**: plug-and-play with other LLMs or embedding models.
- **Runtime efficiency**: fast, low-resource design with modularity.

---

## 📊 Evaluation Results

| Model Setup      | Identical (Green) | Equivalent (Yellow) | Incorrect (Red) | Total Accuracy |
|------------------|------------------|----------------------|------------------|----------------|
| **w/o RAG**      | 8                | 8                    | 84               | **16%**        |
| **with RAG**     | 16               | 56                   | 28               | **72%**        |

✔️ RAG significantly boosts both syntactic and semantic correctness  
✔️ Particularly strong in **multi-table joins** and **nested subqueries**

---

## ⚠️ Known Limitations

- 💬 LLM may generate explanatory text along with SQL
- 🔣 Occasional formatting/syntax inconsistencies (e.g., aliasing issues)
- 🕒 Struggles with temporal expressions like date ranges
- 💡 Lacks automatic syntax validation/post-processing

---

## 🔮 Future Work

- ✅ Add a lightweight SQL validator and formatter
- ✂️ Remove extra commentary in output using stricter prompts
- 🧠 Improve alias consistency and temporal parsing
- 🧪 Incorporate semantic post-checking (e.g., query execution validation)
- 🧬 Experiment with better embeddings and retrievers

---

## 📁 File Structure

```bash
.
├── src/                    # Python modules for each pipeline stage
│   ├── preprocess.py       # Schema parsing
│   ├── embed_index.py      # FAISS index builder
│   ├── retriever.py        # Vector similarity search
│   ├── prompt_builder.py   # Prompt formatting
│   ├── generate_sql.py     # LLM inference using Ollama
│   └── evaluate.py         # Evaluation scripts
├── data/                   # Processed schema and test queries
├── results/                # Evaluation outputs and logs
├── report/                 # Final project report (PDF)
└── README.md
