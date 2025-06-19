import os
import openai
import logging

def main(extracted_text: str) -> str:
    try:
        openai.api_key = os.environ["AZURE_OPENAI_KEY"]
        openai.api_base = os.environ["AZURE_OPENAI_ENDPOINT"]
        openai.api_type = "azure"
        openai.api_version = "2023-05-15"
        deployment = os.environ["CHAT_MODEL_DEPLOYMENT_NAME"]
    except KeyError as e:
        raise EnvironmentError(f"Missing required environment variable: {e}")

    try:
        logging.info("Sending extracted text to OpenAI for summarization.")
        response = openai.ChatCompletion.create(
            engine=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
                {"role": "user", "content": f"Summarize this document:\n\n{extracted_text}"}
            ],
            temperature=0.3,
            max_tokens=500
        )

        summary = response.choices[0].message.content.strip()
        logging.info("Summary successfully generated.")
        return summary

    except Exception as e:
        logging.error(f"Error while generating summary: {e}")
        raise
