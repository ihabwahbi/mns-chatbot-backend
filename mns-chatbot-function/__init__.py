import azure.functions as func
import logging
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(json.dumps({"message": "Invalid input. Please ensure your request is properly formatted."}), status_code=400, mimetype="application/json")

    prompt = req_body.get('prompt')
    if not prompt:
        # Return a more specific message if the prompt is empty or not provided
        return func.HttpResponse(json.dumps({"message": "Please ask a question."}), mimetype="application/json", status_code=400)
    elif prompt.strip() == '':
        # Handles cases where prompt is only whitespace
        return func.HttpResponse(json.dumps({"message": "The question appears to be empty. Please ask a meaningful question."}), mimetype="application/json", status_code=400)
    else:
        # Process the prompt and generate a response
        response_message = json.dumps({"message": "I am still getting developed, be patient! I'll get smarter I promise!"})
        return func.HttpResponse(response_message, mimetype="application/json", status_code=200)
