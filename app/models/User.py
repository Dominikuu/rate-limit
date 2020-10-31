from marshmallow import fields, Schema
import uuid
import datetime
from . import db, bcrypt
from app.models.Pair import PairSchema


class UserModel(db.Model):
    """
    User Model
    """

    # table name
    __tablename__ = 'users'

    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_digest = db.Column(db.String(128), nullable=False)
    created_time = db.Column(db.DateTime)
    modified_time = db.Column(db.DateTime)

    db.relationship('PairModel', backref='users')

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.id = str(uuid.uuid4())
        self.name = data.get('name')
        self.email = data.get('email')
        self.password_digest = self.__generate_hash(data.get('password'))
        self.created_time = datetime.datetime.utcnow()
        self.modified_time = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password_digest = self.__generate_hash(value)
            setattr(self, key, item)
        self.modified_time = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)

    @staticmethod
    def get_user_by_email(value):
        return UserModel.query.filter_by(email=value).first()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr(self):
        return '<id {}>'.format(self.id)


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    created_time = fields.DateTime(dump_only=True)
    modified_time = fields.DateTime(dump_only=True)
    pairs = fields.Nested(PairSchema, many=True)
