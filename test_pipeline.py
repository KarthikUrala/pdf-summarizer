import os
import json
from extract_text import main as extract_text
from summarize_text import main as summarize_text
from save_summary import main as save_summary

# Load environment variables from local.settings.json
with open("local.settings.json", encoding="utf-8") as f:
    config = json.load(f)
    for key, value in config["Values"].items():
        os.environ[key] = value

# Confirm required environment variables
print("🔍 ENV VAR CHECK")
print("COGNITIVE_SERVICES_ENDPOINT =", os.environ.get("COGNITIVE_SERVICES_ENDPOINT", "❌ Missing"))
print("AZURE_OPENAI_KEY =", os.environ.get("AZURE_OPENAI_KEY", "❌ Missing"))
print("BLOB_STORAGE_ENDPOINT =", os.environ.get("BLOB_STORAGE_ENDPOINT", "❌ Missing"))

# Start pipeline
blob_name = "sample.pdf"

print("⏳ Extracting text...")
extracted = extract_text(blob_name)
print("✅ Text extracted.")

print("⏳ Summarizing...")
summary = summarize_text(extracted)
print("✅ Summary generated.")

print("⏳ Uploading summary...")
result = save_summary({"summary": summary, "filename": blob_name})
print("✅ Upload result:", result)
