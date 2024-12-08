from flask import jsonify
from app import app, render_template, request, IMAGE_DIR
import os
import time
from sqlalchemy import create_engine, text
from helpers import file_upload
from routes.product import productList

# Create the engine
engine = create_engine(
    "postgresql+psycopg2://postgres:12345@localhost:5432/flask_ss20"
)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)

# Ensure the IMAGE_DIR ends with a slash
IMAGE_DIR = os.path.join(IMAGE_DIR, 'product')


@app.route('/pos')
def pos():
    return render_template('pos/pos.html')



