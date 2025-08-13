from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "This is a basic flask application"

def start_server():
    print("starting flask server")
    app.run(debug=True, port=8001)


if __name__ == "__main__":
    start_server()
