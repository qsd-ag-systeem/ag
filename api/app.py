from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
import webbrowser

from api.routes.cross_search import cross_search
from api.routes.datasets import get
from api.routes.delete import delete
from api.routes.directories import directories
from api.routes.enroll import cancel, enroll
from api.routes.export import export
from api.routes.get_image import get_image
from api.routes.import_dataset import import_dataset
from api.routes.search import search

app = Flask(
    __name__,
    static_url_path='',
    static_folder='../web/dist',
)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# API routes
app.add_url_rule('/datasets', 'datasets', get)
app.add_url_rule('/search', 'search', search, methods=['POST'])
app.add_url_rule('/cross-search', 'cross-search', cross_search, methods=['POST'])
app.add_url_rule('/import', 'import', import_dataset, methods=['POST'])
app.add_url_rule('/export', 'export', export, methods=['POST'])
app.add_url_rule('/delete', 'delete', delete, methods=['POST'])
app.add_url_rule('/image/<path:path>', 'image', get_image)

# Directories
app.add_url_rule('/directories', 'directories', directories)
app.add_url_rule('/directories/', 'directories', directories)
app.add_url_rule('/directories/<path:subpath>', 'directories', directories)


@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory('./../web/dist/', 'index.html')


socketio.on_event("enroll", enroll)
socketio.on_event("cancel", cancel)


def run(host: str = '0.0.0.0', port: int = 8080, debug: bool = False):
    webbrowser.open(f"http://{host}:{port}")
    socketio.run(app, host=host, port=port, debug=debug)
