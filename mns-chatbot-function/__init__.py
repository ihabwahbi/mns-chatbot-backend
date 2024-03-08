import azure.functions as func
import logging
import json
from utils.openai.openai_manager import openai_handle_initial_msg

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(json.dumps({"message": "Invalid input. Please ensure your request is properly formatted."}), status_code=400, mimetype="application/json")

    prompt = req_body.get('prompt', '')
    thread_id = req_body.get('threadId', None)  # Extract threadId from the request

    if not prompt:
        # Return a more specific message if the prompt is empty or not provided
        return func.HttpResponse(json.dumps({"message": "Please ask a question."}), mimetype="application/json", status_code=400)
    elif prompt.strip() == '':
        # Handles cases where prompt is only whitespace
        return func.HttpResponse(json.dumps({"message": "The question appears to be empty. Please ask a meaningful question."}), mimetype="application/json", status_code=400)
    else:
        # Process the prompt and generate a response using the existing or new thread ID
        response, used_thread_id = openai_handle_initial_msg(prompt, thread_id)  # Pass thread_id to the function
        response_message = json.dumps({"message": response, "threadId": used_thread_id})
        return func.HttpResponse(response_message, mimetype="application/json", status_code=200)
