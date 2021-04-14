import time

#from datetime import datetime
from flask import Flask
from flask import redirect, url_for, request

# TA email: yogolan@ucsc.edu

# instance of flask web app
app = Flask(__name__)

# sample json format
data = {
    "person1": {"name": "rick", "age": 16},
    "person2": {"name": "astley", "age": 65}
}    

# .\venv\Scripts\activate
# gives the route to the function
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # could check the json to determine which function to implement
        pass
    return "West virgina Country Roads"

@app.route("/movies", methods=['GET'])
def movies():
    return data

@app.route("/search")
def search():
    return "search"

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        pass
    return "login"

@app.route("/time")
def time():
    return {"time": time.time()}

if __name__ == "__main__":
    app.run(debug=True)
