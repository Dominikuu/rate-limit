from marshmallow import fields, Schema
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import PrimaryKeyConstraint, ForeignKeyConstraint, UniqueConstraint
import uuid
import datetime
from . import db, bcrypt


class PairModel(db.Model):
    """
    Pair Model
    """
    # table name
    __tablename__ = 'pairs'

    user_id_one = db.Column(db.String(128))

    user_id_two = db.Column(db.String(128))
    
    __table_args__ = (
        UniqueConstraint('user_id_one', name='pairs_u1'),
        PrimaryKeyConstraint('user_id_one', 'user_id_two', name='pairs_pk'),
        ForeignKeyConstraint(('user_id_one',), ["users.id"], name="pairs_fk1", onupdate="CASCADE", ondelete="CASCADE"),
        ForeignKeyConstraint(('user_id_two',), ["users.id"], name="pairs_fk2", onupdate="CASCADE", ondelete="CASCADE"),
        {})

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.user_id_one = data.get('user_id_one')
        self.user_id_two = data.get('user_id_two')

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            print(str(e))
            db.session.rollback()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    @staticmethod
    def get_all_pairs():
        return PairModel.query.all()

    @staticmethod
    def get_one_pair(pairs):
        return PairModel.query.get(pairs)

    def __repr(self):
        return '<id {}>'.format(self.user_id_one)


class PairSchema(Schema):
    user_id_one = fields.Str(required=True)
    user_id_two = fields.Str(required=True)