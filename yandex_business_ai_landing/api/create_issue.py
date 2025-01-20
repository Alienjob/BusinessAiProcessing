from flask import jsonify
from yandex_business_ai_landing.model import ReviewIssue
from yandex_business_ai_landing.extensions import executor, db
import datetime

def createIssue(params, request_id, user_id):
    # Parse user ID (convert from string to integer)
    user_id_int = int(user_id)

    review_id = None
    review_author = None
    review_time = None
    review_rate = None
    review_text = None

    # Extract the operation_id from the params list
    for param in params:
        if param.get('name') == 'review_id':
            review_id = param.get('value')
            
        if param.get('name') == 'review_author':
            review_author = param.get('value')
            
        if param.get('name') == 'review_time':
            review_time = int(param.get('value'))
            
        if param.get('name') == 'review_rate':
            review_rate = int(param.get('value'))
            
        if param.get('name') == 'review_text':
            review_text = param.get('value')
            

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

    review_time_parsed = datetime.datetime.utcfromtimestamp(review_time / 1000.0)

    issue = ReviewIssue( 
        user_id=user_id_int, 
        review_id=review_id,
        review_author=review_author, 
        review_time=review_time_parsed, 
        review_rate=review_rate, 
        review_text=review_text, 
        company_story='', 
        company_response=None,
        status='draft'
    )

    db.session.add(issue)
    db.session.commit()
                
    return jsonify({
        'jsonrpc': '2.0',
        'result': {
            'id': issue.id
        },
        'id': request_id
    })