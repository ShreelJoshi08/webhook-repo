from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)

# -------------------------------------------------------------------
# MongoDB Configuration
# -------------------------------------------------------------------

# Fetch MongoDB URI from environment variable
mongo_uri = os.getenv("MONGO_URI")

# Create MongoDB client
client = MongoClient(mongo_uri)

# Select database and collection
db = client["github_webhooks"]
collection = db["events"]


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.route("/")
def home():
    """
    Renders the main UI page.
    The frontend polls the /events endpoint every 15 seconds.
    """
    return render_template("index.html")


@app.route("/webhook", methods=["POST"])
def webhook():
    """
    GitHub Webhook Endpoint.

    This endpoint receives GitHub events (push, pull_request).
    It extracts only the required minimal data and stores it in MongoDB.
    """

    data = request.json
    event_type = request.headers.get("X-GitHub-Event")

    # Basic validation for incoming payload
    if not data or not event_type:
        return jsonify({"error": "Invalid payload"}), 400

    # ---------------------------------------------------------------
    # Handle PUSH event
    # ---------------------------------------------------------------
    if event_type == "push":
        author = data["pusher"]["name"]
        to_branch = data["ref"].split("/")[-1]

        collection.insert_one({
            "author": author,
            "action": "push",
            "from_branch": None,
            "to_branch": to_branch,
            "timestamp": datetime.now(timezone.utc)
        })

    # ---------------------------------------------------------------
    # Handle PULL REQUEST and MERGE events
    # ---------------------------------------------------------------
    elif event_type == "pull_request":
        pr = data["pull_request"]

        author = pr["user"]["login"]
        from_branch = pr["head"]["ref"]
        to_branch = pr["base"]["ref"]

        # If the pull request is merged, classify it as a "merge" event
        action_type = "merge" if pr.get("merged") else "pull_request"

        collection.insert_one({
            "author": author,
            "action": action_type,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": datetime.now(timezone.utc)
        })

    return jsonify({"status": "received"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    """
    Returns the latest 10 events sorted by timestamp (descending).
    This endpoint is polled by the frontend every 15 seconds.
    """

    events = list(collection.find().sort("timestamp", -1).limit(10))

    formatted_events = []

    for event in events:
        formatted_events.append({
            "author": event["author"],
            "action": event["action"],
            "from_branch": event["from_branch"],
            "to_branch": event["to_branch"],
            "timestamp": event["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")
        })

    return jsonify(formatted_events)




if __name__ == "__main__":
    
    app.run()