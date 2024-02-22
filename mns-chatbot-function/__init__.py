import azure.functions as func
import logging
import json
import psycopg2
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(json.dumps({"message": "Invalid input. Please ensure your request is properly formatted."}), status_code=400, mimetype="application/json")

    prompt = req_body.get('prompt', '')
    if not prompt:
        # Return a more specific message if the prompt is empty or not provided
        return func.HttpResponse(json.dumps({"message": "Please ask a question."}), mimetype="application/json", status_code=400)
    elif prompt.strip() == '':
        # Handles cases where prompt is only whitespace
        return func.HttpResponse(json.dumps({"message": "The question appears to be empty. Please ask a meaningful question."}), mimetype="application/json", status_code=400)
    else:
        # Process the prompt and generate a response
        response = get_material_info(prompt)
        response_message = json.dumps({"message": response})
        return func.HttpResponse(response_message, mimetype="application/json", status_code=200)
    
def get_material_info(material_id):
    # Database connection parameters from environment variables
    conn_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASS'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }
    # SQL query to execute
    query = """
        SELECT material_description, plant, soh
        FROM "material-soh"
        WHERE material = %s;
    """
    
    try:
        # Connect to your database
        print(conn_params)
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Execute the query
        cursor.execute(query, (material_id,))
        result = cursor.fetchall()
        
        # Convert query result to a more friendly format, if result is not empty
        if result:
            response = [{"material_description": row[0], "plant": row[1], "soh": str(row[2])} for row in result]
        else:
            response = []
        
        # Clean up
        cursor.close()
        conn.close()
        
        return response
    except Exception as e:
        print(f"Database query failed: {e}")
        return None
