# 📄 Intelligent PDF Summarizer (Azure Serverless App)

This project is a serverless application built with Azure Functions in Python. It performs the following automated pipeline:

1. **Uploads a PDF document to Azure Blob Storage**
2. **Extracts text using Azure Form Recognizer**
3. **Summarizes the extracted text using Azure OpenAI (GPT-4.1)**
4. **Saves the generated summary back to Blob Storage**

---

## 🧠 Key Azure Services Used

| Service | Purpose |
|--------|---------|
| **Azure Blob Storage** | Stores input PDF and output summary |
| **Azure Form Recognizer** | Extracts text from uploaded PDFs |
| **Azure OpenAI** | Summarizes the extracted text using GPT |
| **Azure Durable Functions** | Orchestrates the multi-step process serverlessly |

---

## 📂 Project Structure

├── extract_text.py # Extracts PDF content using Form Recognizer

├── summarize_text.py # Summarizes extracted content via OpenAI

├── save_summary.py # Saves the summary to Blob storage

├── test_pipeline.py # Manual test script for the pipeline

├── requirements.txt # Python dependencies

├── local.settings.json # Local environment variables

├── host.json # Azure Function host config

└── sample.pdf # Sample PDF for testing


---

## ⚙️ How It Works

### 1. Upload PDF to `input` container on Blob Storage
A file like `sample.pdf` is uploaded to:


### 2. Form Recognizer analyzes the document
Triggered by Azure Function, sending the PDF to:


### 3. GPT Summarizes Extracted Text
The text is summarized using your Azure OpenAI deployment of GPT-4.1.

### 4. Summary Saved Back to `output` Container
A file like `sample_summary.txt` is saved back to Blob Storage.

---

## ✅ Setup

### Prerequisites
- Python 3.10+
- Azure Subscription
- Azure Resources:
  - Azure Blob Storage
  - Form Recognizer (Cognitive Services)
  - Azure OpenAI (with GPT deployment)
- Visual Studio Code + Azure Functions Extension

## Update local.settings.json

Make sure this file contains your environment credentials:


{
"Values": {

    "AzureWebJobsStorage": "<your-storage-connection-string>",
    
    "COGNITIVE_SERVICES_ENDPOINT": "<your-form-recognizer-endpoint>",
    
    "AZURE_OPENAI_ENDPOINT": "<your-openai-endpoint>",
    
    "AZURE_OPENAI_KEY": "<your-openai-key>",
    
    "CHAT_MODEL_DEPLOYMENT_NAME": "gpt-4.1"
    
  }
}

## To Test Locally

python test_pipeline.py

## Status

✅ Project runs end-to-end locally using the test script

⚠️ Azure Functions triggers can be enabled for full deployment
