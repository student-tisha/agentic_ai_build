import threading
import subprocess
import webbrowser
import time
import http.server
import socketserver
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def run_api():
    subprocess.run(["python", "api_server.py"])


def run_static_server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8000), handler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    static_thread = threading.Thread(target=run_static_server, daemon=True)
    static_thread.start()

    time.sleep(2)
    webbrowser.open("http://localhost:8000/index.html")

    print("Both servers running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down.")