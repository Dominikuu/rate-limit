from flask_caching import Cache
from app.extension.session import session  # noqa
from app.extension.socketio import socket_io  # noqa

cache = Cache()