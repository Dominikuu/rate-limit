from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import app_config


app = Flask(__name__)
env_name = 'dev'
app.config.from_object(app_config[env_name])

# initialize our db
db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt()