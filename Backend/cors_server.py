# server.py
from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# --- Configuration ---
PORT = 8001
DIRECTORY_TO_SERVE = "data"
# -------------------

app = Flask(__name__)
CORS(app) # Handles all CORS and OPTIONS requests automatically

# Get the absolute path to the data directory
DATA_DIR = os.path.abspath(DIRECTORY_TO_SERVE)

@app.route('/<path:path>')
def serve_files(path):
    """Serves any file from the 'data' directory."""
    return send_from_directory(DATA_DIR, path)

if __name__ == '__main__':
    print(f"✅ Server started.")
    print(f"📁 Serving files from: {DATA_DIR}")
    print(f"🔗 Listening on: http://localhost:{PORT}")
    print("\nPress Ctrl+C to stop the server.")
    app.run(port=PORT)