# server.py
import http.server
import socketserver
import os

# --- Configuration ---
PORT = 8001
# This is the directory that will be served. We want to serve the 'data' folder.
DIRECTORY_TO_SERVE = "data"
# -------------------

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # This line is key: it tells the server to look inside the DIRECTORY_TO_SERVE
        # instead of the directory where you run the script.
        super().__init__(*args, directory=DIRECTORY_TO_SERVE, **kwargs)

    def end_headers(self):
        # This function adds the CORS headers to every response.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

    def do_OPTIONS(self):
        # Some libraries send a "preflight" OPTIONS request to check CORS rules.
        # This method handles that request.
        self.send_response(204) # 204 No Content
        self.end_headers()


# --- Main execution ---
# Set the working directory to the location of this script to ensure paths are correct
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
    print(f"✅ Server started.")
    print(f"📁 Serving files from the '{DIRECTORY_TO_SERVE}' directory.")
    print(f"🔗 Listening on: http://localhost:{PORT}")
    print("\nPress Ctrl+C to stop the server.")
    httpd.serve_forever()