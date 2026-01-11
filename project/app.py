from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from dotenv import load_dotenv
from datetime import datetime
import os
import re

# Load environment variables
load_dotenv()

# App setup
app = Flask(__name__)

# MongoDB connection
MONGODB_URI = os.getenv("mongodb+srv://upidemail_db_user:qr7ri4OZVShpEct6@cluster0.6esw5ow.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGODB_URI)

db = client["newsletter"]
emails_collection = db["emails"]

# Ensure unique emails
emails_collection.create_index("email", unique=True)

# Email validation
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Health check
@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "API running"}), 200

# Collect email endpoint
@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    email = data.get("email", "").lower().strip()

    if not email or not is_valid_email(email):
        return jsonify({"error": "Invalid email"}), 400

    try:
        emails_collection.insert_one({
            "email": email,
            "created_at": datetime.utcnow(),
            "confirmed": False,
            "source": "api"
        })
        return jsonify({"message": "Email subscribed successfully"}), 201

    except DuplicateKeyError:
        return jsonify({"message": "Email already subscribed"}), 200

# Get all emails (admin use)
@app.route("/emails", methods=["GET"])
def get_emails():
    emails = list(
        emails_collection.find({}, {"_id": 0, "email": 1, "created_at": 1})
    )
    return jsonify(emails), 200

if __name__ == "__main__":
    app.run(debug=True)