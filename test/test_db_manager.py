# test_db_manager.py
from utils.database.db_manager import get_material_info

def test_get_material_info():
    material_id = "B012828"
    result = get_material_info(material_id)
    print("Test Result:", result)

if __name__ == "__main__":
    test_get_material_info()
