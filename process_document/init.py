# process_document/__init__.py
import azure.functions as func
import azure.durable_functions as df

def main(blob: func.InputStream, starter: str):
    client = df.DurableOrchestrationClient(starter)
    instance_id = client.start_new("orchestrator_function", None, blob.name)
    return client.create_check_status_response(None, instance_id)
