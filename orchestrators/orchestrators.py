import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    filename = context.get_input()
    
    # Step 1: Extract text
    extracted_text = yield context.call_activity("extract_text", filename)
    
    # Step 2: Summarize it
    summary = yield context.call_activity("summarize_text", extracted_text)
    
    return summary

main = df.Orchestrator.create(orchestrator_function)
