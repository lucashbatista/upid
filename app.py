
from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
import datetime
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")

# Configure MongoDB connection
# Replace with your MongoDB connection string
# For local: "mongodb://localhost:27017/"
# For Atlas: "mongodb+srv://<username>:<password>@cluster.mongodb.net/?"
MONGO_URI = "mongodb+srv://upidemail_db_user:qr7ri4OZVShpEct6@cluster0.6esw5ow.mongodb.net/?appName=Cluster0" 
DB_NAME = "newsletterDb"
COLLECTION_NAME = "newsletterDb"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
subscribers_collection = db[COLLECTION_NAME]

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email", "").lower().strip()

    if not email:
        flash("Please enter a valid email")
        return redirect("/")

    try:
        subscribers.insert_one({
            "email": email,
            "subscribed_at": datetime.utcnow()
        })
        flash("Thanks for subscribing!")
    except:
        flash("You're already subscribed")

    return redirect("/")


@app.route('/success')
def success():
    return "You have successfully subscribed to the newsletter!"

if __name__ == '__main__':
    # Ensure a 'templates' folder exists in the same directory as app.py
    # and index.html is inside it.
    app.run(debug=True)
