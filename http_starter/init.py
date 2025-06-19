import azure.functions as func
import azure.durable_functions as df

def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    blob_name = req.params.get("filename")

    if not blob_name:
        return func.HttpResponse("Missing 'filename' query parameter", status_code=400)

    # This must match the name used in df.Orchestrator.create()
    instance_id = client.start_new("orchestrator_function", None, blob_name)

    return client.create_check_status_response(req, instance_id)
