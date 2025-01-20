from flask import jsonify
from yandex_business_ai_landing.model import LongOperation
from yandex_business_ai_landing.extensions import executor, db

def getResult(params, request_id, user_id):
    # Parse user ID (convert from string to integer)
    user_id_int = int(user_id)

    # Extract the operation_id from the params list
    operation_id = None
    for param in params:
        if param.get('name') == 'operation_id':
            operation_id = param.get('value')
            break

    if not operation_id:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': -32602,
                'message': 'Invalid params',
                'data': 'operation_id is required'
            },
            'id': request_id
        })            

    operation = LongOperation.query.filter_by(id=operation_id, user_id=user_id_int).first()
    if operation is None:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': -32602,
                'message': 'Invalid operation ID'
            },
            'id': request_id
        })

    return jsonify({
        'jsonrpc': '2.0',
        'result': {
            'id': operation.id,
            'status': operation.status,
            'response': operation.response,
            'error': operation.error
        },
        'id': request_id
    })
