from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return {
        "message": "Hello, World!"
    }

@app.route('/enroll', methods=['POST'])
def enroll():
    return {
        "message": "Enroll"
    }

@app.errorhandler(404)
def page_not_found(e):
    return {
        "message": "Page not found"
    }, 404

def run():
    app.run(host='0.0.0.0', port=5000, debug=True)