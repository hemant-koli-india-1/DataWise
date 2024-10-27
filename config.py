import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
csv_path_file = os.getenv("csv_path_file")