from flask import Flask
from flask import session
from flask import request
from flask import g, url_for
import redis
import os, sys

from models import bcrypt, db
from router.user import user_api as user_blueprint
from router.pair import pair_api as pair_blueprint
from config import app_config

env_mode = os.environ['ENV_MODE']

sys.path.append(os.path.dirname(__file__) + os.sep + '../')

app = Flask(__name__)
app.config.from_object(app_config[env_mode])

# I am using a SHA1 hash. Use a more secure algo in your PROD work
SECRET_KEY = '8cb049a2b6160e1838df7cfe896e3ec32da888d7'
app.secret_key = SECRET_KEY
# initializing bcrypt and db
bcrypt.init_app(app)
db.init_app(app)

app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(pair_blueprint, url_prefix='/pairs')

def init_redis():
    db = redis.StrictRedis(
        host=os.environ["REDIS_HOST"],
        port=os.environ["REDIS_PORT"],
        password="root",
        db=0)
    return db

@app.before_request
def before_request():
    g.redis_db = init_redis()

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')