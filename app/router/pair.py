from http import HTTPStatus
from flask import request, Blueprint, g
from werkzeug.wrappers import Response
from app.models.Pair import PairModel, PairSchema
from shared.ipLimitIntercept import IpLimitIntercept
import json


pair_api = Blueprint('pair_api', __name__)

pair_schema = PairSchema()


@pair_api.route('/', methods=['POST'])
@IpLimitIntercept.ip_limit_intercept
def create(*args, **kwargs):
    """
    Create Pair Function
    """
    req_data = request.get_json()
    data = pair_schema.load(req_data)
    
    error = None
    if error:
        return custom_response(error, HTTPStatus.BAD_REQUEST)

    # check if user already exist in the db
    pair_in_db = PairModel.get_one_pair(data)
    # pair_in_db = PairModel.get_one_pair({
    #     "user_id_one": data.get('user_id_one'),
    #     "user_id_two": data.get('user_id_two'),
    # })
    if pair_in_db:
        message = {'error': 'ERR_PAIR_ALREADY_EXISTED'}
        return custom_response(message, HTTPStatus.BAD_REQUEST)
    pair = PairModel(data)
    pair.save()
    
    ser_data = pair_schema.dump(pair)
    return custom_response(ser_data, HTTPStatus.OK, headers=kwargs["headers"])


@pair_api.route('/', methods=['GET'])
@IpLimitIntercept.ip_limit_intercept
# @Auth.auth_required
def get_all(*args, **kwargs):
    """
    Get all pairs
    """
    pairs = PairModel.get_all_pairs()
    ser_pair = pair_schema.dump(pairs, many=True)
    return custom_response(ser_pair, HTTPStatus.OK, headers=kwargs["headers"])

def custom_response(res, status_code, headers=None):
    """
    Custom Response Function
    """
    return Response(
        headers=headers,
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
