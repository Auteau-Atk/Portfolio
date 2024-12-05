from flask import Flask, redirect, url_for, session
from google.oauth2 import id_token
from google.auth.transport import requests
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/")
def home():
    return "Portfolio Home"

@app.route("/login")
def login():
    # Redirect to Google OAuth
    pass  # Implement Google OAuth flow here

@app.route("/callback")
def callback():
    # Handle OAuth callback
    pass

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
