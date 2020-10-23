
import jwt
import os
import datetime
import time
from http import HTTPStatus
from flask import json, Response, request, g
from functools import wraps
from models.User import UserModel
from shared.lua import SCRIPT as lua_script

IPLimitPeriod     = 3600
IPLimitTimeFormat = "2006-01-02 15:04:05"
IPLimitMaximum    = 50
  
class IpLimitIntercept():
    """
    Auth Class
    """

    @staticmethod
    def generate_token(user_id):
        """
        Generate Token Method
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            print("JWT_SECRET_KEY =================", os.getenv('JWT_SECRET_KEY'))
            return jwt.encode(
                payload,
                os.getenv('JWT_SECRET_KEY'),
                'HS256'
            ).decode("utf-8")
        except Exception as e:
            return Response(
                mimetype="application/json",
                response=json.dumps({'error': 'error in generating user token'}),
                status=400
            )

    @staticmethod
    def decode_token(token):
        """
        Decode token method
        """
        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as e1:
            re['error'] = {'message': 'token expired, please login again'}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {'message': 'Invalid token, please try again with a new token'}
            return re

    
    # decorator
    @staticmethod
    def ip_limit_intercept(func):
        """
        IP limit intercept decorator
        """
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            now = int(time.time())
            result = None
            with g.redis_db.pipeline() as pipe:
                try:
                    script = g.redis_db.register_script(lua_script)
                    script(keys=[request.remote_addr], args=[now, IPLimitMaximum, IPLimitPeriod], client=pipe)
                    result = pipe.execute()[0]
                except Exception as e:
                    return Response(
                        mimetype="application/json",
                        response=json.dumps({'error': e}),
                        status=HTTPStatus.BAD_REQUEST
                    )

            remaining, reset = result[0], result[1]
            
            if remaining == -1:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': "ERR_FREQUENT_REQUEST"}),
                    status=HTTPStatus.TOO_MANY_REQUESTS
                )
            kwargs['headers'] = {
                "X-RateLimit-Remaining": remaining,
                "X-RateLimit-Reset": reset
            }   
            return func(*args, **kwargs)

        return decorated_auth