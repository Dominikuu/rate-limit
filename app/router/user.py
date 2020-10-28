from http import HTTPStatus
from flask import request, Blueprint, g
from werkzeug.wrappers import Response
from app.models.User import UserModel, UserSchema
from app.shared.auth import Auth
import json

user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()

@user_api.route('/', methods=['POST'])
def create():
    """
    Create User Function
    """
    req_data = request.get_json()
    data = user_schema.load(req_data)
    error = None
    if error:
        return custom_response(error, HTTPStatus.BAD_REQUEST)

    # check if user already exist in the db
    user_in_db = UserModel.get_user_by_email(data.get('email'))
    if user_in_db:
        message = {'error': 'User already exist, please supply another email address'}
        return custom_response(message,  HTTPStatus.BAD_REQUES)

    user = UserModel(data)
    user.save()
    
    ser_data = user_schema.dump(user)
    token = Auth.generate_token(ser_data.get('id'))
    print(type(token))
    if type(token) is not str:
        return token
    return custom_response({'jwt_token': json.dumps(token)}, HTTPStatus.OK)


@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    """
    Get all users
    """
    users = UserModel.get_all_users()
    ser_users = user_schema.dump(users, many=True)
    return custom_response(ser_users, HTTPStatus.OK)


@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
    """
    Get a single user
    """
    user = UserModel.get_one_user(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, HTTPStatus.NOT_FOUND)

    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, HTTPStatus.OK)


@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
    """
    Update me
    """
    req_data = request.get_json()
    data, error = user_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, HTTPStatus.BAD_REQUES)

    user = UserModel.get_one_user(g.user.get('id'))
    user.update(data)
    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, HTTPStatus.OK)


@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
    """
    Delete a user
    """
    user = UserModel.get_one_user(g.user.get('id'))
    user.delete()
    return custom_response({'message': 'deleted'}, HTTPStatus.NO_CONTENT)


@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
    """
    Get me
    """
    user = UserModel.get_one_user(g.user.get('id'))
    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, HTTPStatus.OK)


@user_api.route('/login', methods=['POST'])
def login():
    """
    User Login Function
    """
    req_data = request.get_json()

    data, error = user_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, HTTPStatus.BAD_REQUEST)
    if not data.get('email') or not data.get('password'):
        return custom_response({'error': 'you need email and password to sign in'}, HTTPStatus.BAD_REQUEST)
    user = UserModel.get_user_by_email(data.get('email'))
    if not user:
        return custom_response({'error': 'invalid credentials'}, HTTPStatus.BAD_REQUEST)
    if not user.check_hash(data.get('password')):
        return custom_response({'error': 'invalid credentials'}, HTTPStatus.BAD_REQUEST)
    ser_data = user_schema.dump(user).data
    token = Auth.generate_token(ser_data.get('id'))
    return custom_response({'jwt_token': token}, HTTPStatus.OK)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
