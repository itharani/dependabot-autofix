from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def home():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    return response.text  # Bug: Should return JSON, not text

if __name__ == "__main__":
    app.run(debug=True)
