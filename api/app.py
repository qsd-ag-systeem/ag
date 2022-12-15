from flask import Flask
from api.routes.hello import index
from api.routes.enroll import enroll

app = Flask(__name__)

# API routes
app.add_url_rule('/', 'index', index)
app.add_url_rule('/enroll', 'enroll', enroll, methods=['POST'])


@app.errorhandler(404)
def page_not_found(e):
    return {
               "message": "Page not found"
           }, 404


def run():
    app.run(host='0.0.0.0', port=5000, debug=True)
