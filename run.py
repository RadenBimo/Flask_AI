from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)