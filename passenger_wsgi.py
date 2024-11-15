# passenger_wsgi.py

import sys
import os

# Add the project directory to the sys.path
project_home = u'/home/anaehugo/fugaemfamilia/backend_v2/passenger_wsgi.py'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set the environment variable for the Flask app
os.environ['FLASK_APP'] = 'app.py'

# Import the Flask app
from app import app as application
