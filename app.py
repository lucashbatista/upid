from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
from pathlib import Path
import os
import certifi
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from datetime import datetime

# -------------------------
# Load .env
# -------------------------
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("❌ MongoDB Atlas URI NOT loaded")

# -------------------------
# Connect to MongoDB Atlas
# -------------------------
client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)

# Test connection
try:
    client.admin.command("ping")
    print("✅ Connected to MongoDB Atlas")
except Exception as e:
    raise RuntimeError(f"❌ Cannot connect to MongoDB Atlas: {e}")

db = client["upid"]
newsletter = db["newsletter"]
newsletter.create_index("email", unique=True)
print("✅ Newsletter collection ready with unique index on 'email'")

# -------------------------
# Create Flask app
# -------------------------
app = Flask(__name__)

# -------------------------
# Serve the newsletter page
# -------------------------
@app.route("/", methods=["GET"])
def index():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Newsletter Signup</title>
      <style>
        body { font-family: Arial, sans-serif; padding: 2rem; background: #f9f9f9; }
        .container { max-width: 400px; margin: auto; background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input[type="email"] { width: 100%; padding: 0.5rem; margin-bottom: 1rem; border-radius: 5px; border: 1px solid #ccc; }
        button { padding: 0.5rem 1rem; border: none; background: #4CAF50; color: white; border-radius: 5px; cursor: pointer; }
        button:hover { background: #45a049; }
        .message { margin-top: 1rem; font-weight: bold; }
        .success { color: green; }
        .error { color: red; }
      </style>
    </head>
    <body>
      <div class="container">
        <h2>Subscribe to our Newsletter</h2>
        <input type="email" id="email" placeholder="Enter your email" required />
        <button id="subscribeBtn">Subscribe</button>
        <div id="message" class="message"></div>
      </div>

      <script>
        const subscribeBtn = document.getElementById("subscribeBtn");
        const emailInput = document.getElementById("email");
        const messageDiv = document.getElementById("message");

        subscribeBtn.addEventListener("click", async () => {
          const email = emailInput.value.trim();
          messageDiv.textContent = "";
          messageDiv.className = "message";

          if (!email) {
            messageDiv.textContent = "Please enter an email.";
            messageDiv.classList.add("error");
            return;
          }

          try {
            const res = await fetch("/subscribe", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ email })
            });

            const data = await res.json();

            if (res.ok || res.status === 200) {
              messageDiv.textContent = data.message || "Subscribed successfully!";
              messageDiv.classList.add("success");
              emailInput.value = "";
            } else {
              messageDiv.textContent = data.error || "Something went wrong.";
              messageDiv.classList.add("error");
            }

          } catch (err) {
            messageDiv.textContent = "Network error. Please try again.";
            messageDiv.classList.add("error");
            console.error("Network error:", err);
          }
        });
      </script>
    </body>
    </html>
    """
    return render_template_string(html)

# -------------------------
# /subscribe endpoint
# -------------------------
@app.route("/subscribe", methods=["POST"])
def subscribe():
    print("➡️ /subscribe called")
    try:
        data = request.get_json()
        print("📦 Incoming data:", data)

        if not data or "email" not in data:
            return jsonify({"error": "Email is required"}), 400

        email = data["email"].strip().lower()
        if "@" not in email or "." not in email:
            return jsonify({"error": "Invalid email"}), 400

        newsletter.insert_one({"email": email, "created_at": datetime.utcnow()})
        print("✅ Email inserted into MongoDB")
        return jsonify({"message": "Subscribed successfully"}), 201

    except DuplicateKeyError:
        print("⚠️ Duplicate email attempted")
        return jsonify({"message": "Email already subscribed"}), 200

    except Exception as e:
        print("🔥 FULL ERROR:", repr(e))
        return jsonify({"error": "Server error"}), 500

# -------------------------
# Run Flask app
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
