import psycopg2
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

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