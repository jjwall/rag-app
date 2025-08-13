from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive_data', methods=['GET'])
def receive_data():
    try:
        data = '''
            {
                "text": "This is test #3"
            }
            '''
            
        return jsonify({'data': data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/send_data', methods=['POST'])
def send_data():
    try:
        # Parse JSON payload from request
        request_data = request.json

        # Extract data from request
        text = request_data['text']

        print(text)
            
        return jsonify({'data_sent': text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return "This is a basic flask application"

def start_server():
    print("starting flask server")
    app.run(debug=True, port=8001)

if __name__ == "__main__":
    start_server()
