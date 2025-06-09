import subprocess
import sys
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Starts the Streamlit server for resume analysis'

    def handle(self, *args, **options):
        try:
            # Get the path to the Streamlit app
            app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app.py')
            
            # Start Streamlit server
            self.stdout.write(self.style.SUCCESS('Starting Streamlit server...'))
            subprocess.run([sys.executable, '-m', 'streamlit', 'run', app_path, '--server.port', '8502'])
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error starting Streamlit server: {str(e)}')) 