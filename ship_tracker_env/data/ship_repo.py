import csv
from data import mongodb_context

db = mongodb_context.create_connection_with_mongodb()
tracking_collection = mongodb_context.get_the_tracking_collection(db)

def get_all_ships_tracking_details_from_db():
    db = mongodb_context.create_connection_with_mongodb()
    collection = mongodb_context.get_the_tracking_collection(db)
    ships_details = collection.find()
    return ships_details
        
def insert_tracking_data(csv_filepath):
    inserted_mmsi = set()
    try:
        with open(csv_filepath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                mmsi =  int(row.get('MMSI'))
                print(mmsi)
                if mmsi not in inserted_mmsi:
                    specific_columns = {
                        'MMSI': mmsi,
                        'VesselName': row.get('VesselName', ''),
                        'BaseDateTime': row.get('BaseDateTime', ''),
                        'LAT': float(row.get('LAT', 0.0)) if row['LAT'] != '' else 0.0,
                        'LON': float(row.get('LON', 0.0)) if row['LON'] != '' else 0.0
                    }
                    tracking_collection.insert_one(specific_columns)
                    inserted_mmsi.add(mmsi)
        return "Values inserted"
    except Exception as e:
        return f"Error {e}"