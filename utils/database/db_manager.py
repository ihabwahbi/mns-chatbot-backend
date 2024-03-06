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
        SELECT material, material_description, plant, planned_req_date, mrp_element_desc, mrp_element_number, mrp_element_item, rec_reqd_quantity, mrp_date, safety_stock, unit_of_measure, standard_price, mrp_element_data, currency
        FROM "md04"
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
            db_output = [
                {
                    "material": row[0],
                    "material_description": row[1],
                    "plant": row[2],
                    "planned_req_date": str(row[3]),
                    "mrp_element_desc": row[4],
                    "mrp_element_number": row[5],
                    "mrp_element_item": row[6],
                    "rec_reqd_quantity": row[7],
                    "mrp_date": str(row[8]),
                    "safety_stock": row[9],
                    "unit_of_measure": row[10],
                    "standard_price": row[11],
                    "mrp_element_data": row[12],
                    "currency": row[13]
        } for row in result
            ]
        else:
            db_output = []
        
        # Clean up
        cursor.close()
        conn.close()
        print("Database output is ", db_output)
        return db_output
    except Exception as e:
        print(f"Database query failed: {e}")
        return None