import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from a .env file (create this file in the same directory)
load_dotenv()

# Get the connection string from an environment variable
# Make sure to replace <username> and <password> in your Atlas connection string with actual credentials
# e.g., in your .env file: CONNECTION_STRING="mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

def get_database():
    """Establishes a connection to the MongoDB Atlas cluster."""
    # Create a connection using MongoClient
    client = MongoClient(CONNECTION_STRING)
    
    # Return the database instance (e.g., 'newsletter' database)
    return client['newsletter']

if __name__ == "__main__":
    # Example usage:
    dbname = get_database()
    print(f"Connected to database: {dbname.name}")
    # You can now access collections, e.g., subscribers = dbname["subscribers"]
