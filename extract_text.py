import logging
import os
import requests
import time

def main(blob_name: str) -> str:
    logging.info(f"Extracting text from blob: {blob_name}")

    # Load from env
    endpoint = os.environ.get("COGNITIVE_SERVICES_ENDPOINT")
    key = os.environ.get("AZURE_FORMRECOGNIZER_KEY")
    blob_url = os.environ.get("BLOB_SAS_URL")


    if not all([endpoint, key, blob_url]):
        raise Exception("Missing one or more required environment variables.")

    form_url = f"{endpoint}/formrecognizer/documentModels/prebuilt-document:analyze?api-version=2023-07-31"
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": key
    }

    body = {
        "urlSource": blob_url
    }

    try:
        response = requests.post(form_url, headers=headers, json=body)
        response.raise_for_status()
        result_url = response.headers["operation-location"]
    except Exception as e:
        logging.error(f"Form Recognizer request failed: {str(e)}")
        raise

    # Polling
    for _ in range(20):
        result = requests.get(result_url, headers=headers).json()
        status = result.get("status")
        if status == "succeeded":
            break
        elif status == "failed":
            raise Exception("Form Recognizer analysis failed.")
        time.sleep(1)
    else:
        raise TimeoutError("Form Recognizer polling timed out.")

    try:
        pages = result["analyzeResult"]["pages"]
        text = " ".join(page.get("content", "") for page in pages)
        return text
    except Exception as e:
        logging.error("Error extracting text from result.")
        raise e
