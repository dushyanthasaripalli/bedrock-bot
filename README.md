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

# 🛠️ Tech Stack:
# Area	            Tool / Service
# LLM               Inference	AWS Bedrock (Claude, Titan)
# Embedding         Model	Amazon Titan / Cohere
# Vector            DB	Amazon OpenSearch / FAISS
# Document          Store	Amazon S3
# Orchestration	    LangChain / Custom Python
# App Layer	        Lambda + API Gateway
# UI (Optional)	    Streamlit or simple HTML



🗂️ Full Project Structure: bedrock-bot/

bedrock-bot/
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   └── index.js
│   ├── build/
│   │   └── index.html
│   ├── package.json
│   └── .gitignore
├── terraform/
│   ├── main.tf
│   └── variables.tf
├── README.md
├── .gitignore
└── .git/
Let’s go piece by piece:

📁 frontend/ — Your React App
This folder contains your frontend UI, built with React.

🔹 frontend/public/
Contains static files like the index.html template.

This is the file that gets served as the HTML shell for your entire app.

Other files like favicon.ico or manifest go here.

🔹 frontend/src/
Your actual React code lives here.

Typical files:

App.js: Your main React component (you edit this most).

index.js: Entry point where React attaches to the public/index.html.

🔹 frontend/package.json
Declares all dependencies, scripts (npm run start, npm run build, etc.).

Example dependencies: react, react-bootstrap, etc.

Also includes app name, version, and scripts.

🔹 frontend/.gitignore
Prevents unnecessary files from being pushed to Git.

Often includes: node_modules/, build/, .env

🔹 frontend/build/ — 💥 Auto-generated
This folder is created when you run npm run build.

Contains the production-ready static files (minified JS, HTML, CSS).

Terraform uses this to upload to S3.

✅ This is the folder Terraform needs to read from for deployment.

📁 terraform/ — Infrastructure-as-Code (AWS Setup)
This folder holds Terraform files that define and deploy your AWS infrastructure.

🔹 terraform/main.tf
Contains the main config: creating S3 bucket, uploading files from frontend/build/, etc.

Includes the aws_s3_bucket, aws_s3_object, provider, and output definitions.

🔹 terraform/variables.tf (optional but common)
Lets you define input variables used in main.tf, like bucket_name, region, etc.

🗃️ Root Files in bedrock-bot/
🔹 .gitignore (Root)
Prevents things like .env, .DS_Store, node_modules, and terraform.tfstate from being tracked by Git.

🔹 README.md
Optional but highly recommended.

Describes what the project does and how to run/deploy it.

🔹 .git/ (hidden)
This is your local Git repo metadata — used for version tracking.

✅ How All This Works Together
Here’s a full flow:

You write frontend UI in frontend/src/

You run npm run build
→ Generates production files into frontend/build/

You run terraform apply
→ Terraform reads from frontend/build/ and uploads to AWS S3

Your React app becomes available via the public S3 URL

🎯 Final Tips
Folder/File	Required?	Why It Matters
frontend/build/	✅	Contains deployable static site
main.tf	✅	Defines infra (bucket, object uploads)
.gitignore	✅	Keeps Git clean from unnecessary files
package.json	✅	Manages dependencies, app metadata, and build/start scripts
index.html	✅	The HTML shell served by S3
App.js	✅	Where you build your actual UI
terraform.tfstate	🔒 Never Git it	Tracks infra state, must be kept secure and local/cloud backed