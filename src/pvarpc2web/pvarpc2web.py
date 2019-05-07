from flask import Blueprint, current_app, request, jsonify
from flask_cors import cross_origin

from .pvaapi import pvaapi
from .exception import InvalidRequest


pvarpc2web = Blueprint('pvarpc2web', __name__)
methods = ('GET', 'POST')


@pvarpc2web.route('/', methods=methods)
@cross_origin()
def pvarpc():
    """PVA RPC gateway url function

    Returns
    -------
    flask.Response
        json formatted metrics response

    Raises
    ------
    InvalidRequest
        if request parameters are missing
    """
    current_app.logger.info(request.headers)
    current_app.logger.info(request.get_json())

    req = request.get_json()
    print('request')
    print(req)

    if request.method == 'GET':
        args = request.args.to_dict()
        try:
            ch_name = args['ch_name']
            del args['ch_name']
        except (KeyError, IndexError) as e:
            raise InvalidRequest('Invalid query', status_code=400,
                                 details={'request': req})
        nturi = False if 'nonturi' in args else True
        if not nturi:
            del args['nonturi']
        query = args

    elif request.method == 'POST':
        try:
            ch_name = req['ch_name']
            query = req['query']
            nturi = req.get('nturi', True)
        except (KeyError, IndexError) as e:
            raise InvalidRequest('Invalid query', status_code=400,
                                 details={'request': req})

    res = pvaapi.rpccall(ch_name, query, nturi)

    return jsonify(res)


@pvarpc2web.errorhandler(InvalidRequest)
def handle_invalid_usage(error):
    """Flask error handler for InvalidRequest

    Parameters
    ----------
    error : exception.InvalidRequest
        error detail

    Returns
    -------
    flask.Response
        json formatted error response
    """

    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
