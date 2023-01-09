from flask import Flask
from flask_cors import CORS

from api.helpers.response import error_response
from api.routes.index import index
from api.routes.enroll import enroll
from api.routes.datasets import get
from api.routes.search import search
from api.routes.directories import directories

app = Flask(__name__)
CORS(app)

# API routes
app.add_url_rule('/', 'index', index)
app.add_url_rule('/datasets', 'datasets', get)
app.add_url_rule('/enroll', 'enroll', enroll, methods=['POST'])
app.add_url_rule('/search', 'search', search, methods=['POST'])

# Directories
app.add_url_rule('/directories', 'directories', directories)
app.add_url_rule('/directories/', 'directories', directories)
app.add_url_rule('/directories/<path:subpath>', 'directories', directories)


@app.errorhandler(404)
def page_not_found(e):
    return error_response('Page not found', 404)


def run(host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
    app.run(host=host, port=port, debug=debug)
