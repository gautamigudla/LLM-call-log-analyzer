from flask import Flask
app = Flask(__name__)

# Assuming data_store is initialized in routes.py
from .routes import data_store

# Other imports as necessary
