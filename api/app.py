from flask import Flask
from api.routes.index import index
from api.routes.enroll import enroll
from api.routes.search import search

app = Flask(__name__)

# API routes
app.add_url_rule('/', 'index', index)
app.add_url_rule('/enroll', 'enroll', enroll, methods=['POST'])
app.add_url_rule('/search', 'search', search, methods=['POST'])


@app.errorhandler(404)
def page_not_found(e):
    return {
               "message": "Page not found"
           }, 404


def run():
    app.run(host='0.0.0.0', port=5000, debug=True)
