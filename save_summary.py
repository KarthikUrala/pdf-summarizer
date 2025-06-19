import os
from azure.storage.blob import BlobServiceClient
import logging

def main(input: dict) -> str:
    summary = input["summary"]
    filename = input["filename"]
    output_filename = f"{os.path.splitext(filename)[0]}_summary.txt"

    try:
        blob_service_client = BlobServiceClient.from_connection_string(os.environ["AzureWebJobsStorage"])
        output_container = blob_service_client.get_container_client("output")

        logging.info(f"Uploading summary to blob: {output_filename}")

        output_container.upload_blob(
            name=output_filename,
            data=summary,
            overwrite=True
        )

        return f"Saved summary to {output_filename}"

    except Exception as e:
        logging.error(f"Failed to upload summary to blob: {e}")
        raise
