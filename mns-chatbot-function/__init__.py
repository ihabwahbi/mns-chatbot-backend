import azure.functions as func
import logging
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    prompt = req.params.get('prompt')
    if not prompt:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            prompt = req_body.get('prompt')

    if prompt:
        response_message = json.dumps({"message": "I am still getting developed, be patient! I'll get smarter I promise!"})
        return func.HttpResponse(response_message, mimetype="application/json", status_code=200)
    else:
        response_message = json.dumps({"message": "How can I help?"})
        return func.HttpResponse(response_message, mimetype="application/json", status_code=200)
