# bedrock-bot
# Ask My Company Docs – GenAI Q&A Assistant using AWS Bedrock + RAG

This project demonstrates how to build a lightweight, scalable GenAI assistant that answers natural language questions from company documents using the Retrieval-Augmented Generation (RAG) framework.

## 💡 Features

- Upload internal policy docs (PDF/TXT)
- Embed with Amazon Titan or Cohere via AWS Bedrock
- Store embeddings in FAISS (or Amazon OpenSearch)
- Ask natural questions — retrieve + generate answers
- Expose as API via AWS Lambda + API Gateway
- Optional: Simple local UI with Streamlit

## 🧱 Tech Stack

- AWS Bedrock (Claude / Titan)
- Amazon S3
- Amazon OpenSearch (or FAISS locally)
- Python + LangChain
- AWS Lambda + API Gateway

## 🚀 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/ask-my-company-docs.git
cd ask-my-company-docs
