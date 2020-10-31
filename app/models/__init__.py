from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import app_config, Development


app = Flask(__name__)
env_name = 'dev'

app.config.from_object(Development)


# initialize our db
db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt()