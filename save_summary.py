import os
from azure.storage.blob import BlobServiceClient
import logging

def main(payload: dict) -> str:
    logging.info("Saving summary to Blob Storage...")

    # Read from environment
    blob_connection_str = os.environ.get("AzureWebJobsStorage")
    blob_base_url = os.environ.get("BLOB_STORAGE_ENDPOINT")

    if not all([blob_connection_str, blob_base_url]):
        raise Exception("Missing AzureWebJobsStorage or BLOB_STORAGE_ENDPOINT in environment variables.")

    filename = payload.get("filename", "output.txt").replace(".pdf", "-summary.txt")
    summary = payload.get("summary", "")

    if not summary:
        raise ValueError("Summary content is empty.")

    try:
        # Connect to blob service
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_str)
        container_name = "output"
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

        # Upload content
        blob_client.upload_blob(summary, overwrite=True)
        logging.info(f"✅ Summary uploaded to container '{container_name}' as '{filename}'")
        return f"{blob_base_url}/{container_name}/{filename}"
    except Exception as e:
        logging.error(f"Failed to upload summary: {str(e)}")
        raise
