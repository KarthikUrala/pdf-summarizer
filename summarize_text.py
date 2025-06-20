import os
import logging
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionMessageParam

def main(text: str) -> str:
    try:
        logging.info("Starting summary generation...")

        # Load credentials from environment variables
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        api_key = os.environ.get("AZURE_OPENAI_KEY")
        deployment = os.environ.get("CHAT_MODEL_DEPLOYMENT_NAME")

        if not all([endpoint, api_key, deployment]):
            raise Exception("Missing one or more required environment variables for OpenAI")

        # Setup Azure OpenAI client
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-02-15-preview",
            azure_endpoint=endpoint
        )

        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": "You are an assistant that summarizes PDF content."
            },
            {
                "role": "user",
                "content": text
            }
        ]

        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logging.error("Error while generating summary:")
        logging.error(str(e))
        raise
