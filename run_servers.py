import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def run_django():
    subprocess.run([sys.executable, 'manage.py', 'runserver'])

def run_streamlit():
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py', '--server.port', '8502'])

if __name__ == '__main__':
    # Start Django server in a separate thread
    django_thread = Thread(target=run_django)
    django_thread.daemon = True
    django_thread.start()

    # Wait for Django server to start
    time.sleep(2)

    # Start Streamlit server in a separate thread
    streamlit_thread = Thread(target=run_streamlit)
    streamlit_thread.daemon = True
    streamlit_thread.start()

    # Wait for Streamlit server to start
    time.sleep(2)

    # Open the Django homepage in the default browser
    webbrowser.open('http://localhost:8000')

    try:
        # Keep the main thread running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        sys.exit(0) 