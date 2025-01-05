import os
import time
import random
import json
from flask import Flask, send_file

app = Flask(__name__)

# Local folder containing PDFs
PDF_DIR = "/app/pdf_files"  # Use this path for Render deployment
STATE_FILE = "/app/state.json"  # File to track selected PDF and last update time

# Function to load the current state (selected PDF and last update time)
def load_state():
    if not os.path.exists(STATE_FILE):
        return {"current_pdf": None, "last_update": 0}
    with open(STATE_FILE, "r") as file:
        return json.load(file)

# Function to save the state
def save_state(state):
    with open(STATE_FILE, "w") as file:
        json.dump(state, file)

# Function to handle daily PDF rotation
def get_daily_pdf():
    state = load_state()
    current_time = time.time()

    # If 24 hours have passed or no PDF is selected
    if current_time - state.get("last_update", 0) > 86400 or not state.get("current_pdf"):
        pdfs = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
        if not pdfs:
            return None  # No PDFs available

        selected_pdf = random.choice(pdfs)
        state["current_pdf"] = selected_pdf
        state["last_update"] = current_time
        save_state(state)

    return state["current_pdf"]

# Route to serve the daily PDF
@app.route("/workout")
def serve_daily_pdf():
    selected_pdf = get_daily_pdf()
    if not selected_pdf:
        return "No PDFs available", 404

    pdf_path = os.path.join(PDF_DIR, selected_pdf)
    return send_file(pdf_path, download_name=selected_pdf, mimetype="application/pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

