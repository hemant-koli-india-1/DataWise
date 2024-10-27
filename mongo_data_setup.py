import pandas as pd
from pymongo import MongoClient
from config import MONGODB_URI, DATABASE_NAME, COLLECTION_NAME

def setup_database():
    # Initialize MongoDB
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Load and process data
    csv_file_path = "resource/sample_data.csv"
    data = pd.read_csv(csv_file_path)
    data['Discount'] = data['Discount'].str.replace('%', '').astype(int)
    data_dict = data.to_dict(orient="records")

    # Insert into MongoDB
    collection.delete_many({})  # Clear collection
    collection.insert_many(data_dict)
    print(f"{len(data_dict)} records inserted.")
