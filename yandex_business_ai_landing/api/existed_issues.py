from flask import jsonify
from yandex_business_ai_landing.model import ReviewIssue
from yandex_business_ai_landing.extensions import executor, db

def existedIssues(params, request_id, user_id):
    # Parse user ID (convert from string to integer)
    user_id_int = int(user_id)

    issues = ReviewIssue.query.filter_by(user_id=user_id_int)
    if issues is None:
        issues = []

    result = []
    for issue in issues:
        result.append({
            'status': issue.status,
            'review_id': issue.review_id,
        })

    return jsonify({
        'jsonrpc': '2.0',
        'result': result,
        'id': request_id
    })