import logging
import os
import requests
import time

def main(blob_name: str) -> str:
    logging.info(f"Extracting text from blob: {blob_name}")

    # Correct environment variable keys
    endpoint = os.environ.get("COGNITIVE_SERVICES_ENDPOINT")
    key = os.environ.get("AZURE_FORMRECOGNIZER_KEY")  # Make sure this key is set in local.settings.json
    blob_base_url = os.environ.get("BLOB_STORAGE_ENDPOINT")

    if not all([endpoint, key, blob_base_url]):
        raise Exception("Missing one or more required environment variables.")

    blob_url = f"{blob_base_url}/input/{blob_name}"
    form_url = f"{endpoint.rstrip('/')}/formrecognizer/documentModels/prebuilt-document:analyze?api-version=2023-07-31"


    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": key
    }

    body = {
        "urlSource": blob_url
    }

    # Submit document for analysis
    try:
        response = requests.post(form_url, headers=headers, json=body)
        response.raise_for_status()
        result_url = response.headers["operation-location"]
    except Exception as e:
        logging.error(f"Form Recognizer request failed: {str(e)}")
        raise

    # Poll the result endpoint
    for _ in range(20):  # Max 20 tries
        result = requests.get(result_url, headers=headers).json()
        status = result.get("status")
        if status == "succeeded":
            logging.info("Form Recognizer analysis succeeded.")
            break
        elif status == "failed":
            logging.error("Form Recognizer analysis failed.")
            raise Exception("Document analysis failed.")
        time.sleep(1)
    else:
        raise TimeoutError("Form Recognizer polling timed out.")

    # Extract text
    try:
        pages = result["analyzeResult"]["pages"]
        text = " ".join(page.get("content", "") for page in pages)
        return text
    except Exception as e:
        logging.error("Error extracting text from result.")
        raise e
