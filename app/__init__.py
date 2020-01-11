"""
Init app package
"""
import os
from flask import Flask, escape

# Get environment variables
GMAP_API_KEY = os.environ.get("GMAP_API_KEY")

app = Flask(__name__)
