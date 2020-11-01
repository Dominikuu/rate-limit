from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import Development,app_config


app = Flask(__name__)
env_mode = 'dev'
app.config.from_object('app.config.' + app_config[env_mode])


# initialize our db
db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt()