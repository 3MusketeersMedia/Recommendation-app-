from flask import flask

app = Flask(__name__)

def home():
    print("home")