from flask import jsonify
from yandex_business_ai_landing.model import LongOperation
from yandex_business_ai_landing.extensions import executor, db
import json

def ping(params, request_id, user_id):
    # Parse user ID (convert from string to integer)
    user_id_int = int(user_id)

   # Convert the params dictionary to a JSON string
    params_json = json.dumps(params, ensure_ascii=False)
    
    # Create a new long operation
    new_operation = LongOperation(
        user_id=user_id_int,
        status='processing',
        request=params_json,
        response=None,
        error=None
    )
    db.session.add(new_operation)
    db.session.commit()

    # Start the background task
    executor.submit(process_long_operation, new_operation.id)

    # Return the CreateOperationResponse
    return jsonify({
        'jsonrpc': '2.0',
        'result': {
            'id': new_operation.id,
            'status': new_operation.status
        },
        'id': request_id
    })

def process_long_operation(operation_id):
    import time
    time.sleep(10)  # Simulate a delay

    operation = LongOperation.query.get(operation_id)
    operation.status = 'done'
    operation.response = 'Operation completed successfully'
    db.session.commit()