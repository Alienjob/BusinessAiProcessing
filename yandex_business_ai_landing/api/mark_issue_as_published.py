from flask import jsonify
from yandex_business_ai_landing.model import ReviewIssue
from yandex_business_ai_landing.extensions import executor, db

def markIssueAsPublished(params, request_id, user_id):
    # Parse user ID (convert from string to integer)
    user_id_int = int(user_id)

    review_id = None

    # Extract the operation_id from the params list
    for param in params:
        if param.get('name') == 'review_id':
            review_id = param.get('value')
            break

    if not review_id:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': -32602,
                'message': 'Invalid params',
                'data': 'review_id is required'
            },
            'id': request_id
        })

    issue = ReviewIssue.query.filter_by(user_id=user_id_int, review_id=review_id).first()
    if issue is None:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': -32602,
                'message': 'Invalid review ID'
            },
            'id': request_id
        })
    issue.status = 'published'
    db.session.commit()

    return jsonify({
        'jsonrpc': '2.0',
        'result': {
            'id': issue.id,
            'status': issue.status,
            'review_id': issue.review_id,
        },
        'id': request_id
    })