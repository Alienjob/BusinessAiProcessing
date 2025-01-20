from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from yandex_business_ai_landing.api.ping import ping
from yandex_business_ai_landing.api.get_result import getResult
from yandex_business_ai_landing.api.answer_review import answerReview
from yandex_business_ai_landing.api.scheduled_post import scheduledPost
from yandex_business_ai_landing.api.mark_post_as_published import markPostAsPublished
from yandex_business_ai_landing.api.existed_issues import existedIssues
from yandex_business_ai_landing.api.create_issue import createIssue
from yandex_business_ai_landing.api.get_issue import getIssue
from yandex_business_ai_landing.api.mark_issue_as_published import markIssueAsPublished

from yandex_business_ai_landing.model import UserPrompts, User

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/jsonrpc', methods=['POST'])
@jwt_required()
def jsonrpc():
    data = request.get_json()
    method = data.get('method')
    params = data.get('params')
    request_id = data.get('id')
    user_id = get_jwt_identity()

    userPrompts = UserPrompts.query.filter_by(user_id=user_id).first()
    prompt = userPrompts.review_prompt if userPrompts else None
    if prompt == '':
        prompt = None

    user = User.query.get(user_id)
    if user is None:
        companyInfo = 'Информация о компании не заполнена'
    else:
        company_name = user.company_name if user.company_name else 'Название компании не указано'
        company_description = user.company_description if user.company_description else 'Описание компании не указано'
        additional_info = user.additional_info if user.additional_info else 'Дополнительная информация не указана'
        companyInfo = f'Название компании: {company_name}\nОписание компании: {company_description}\nДополнительная информация: {additional_info}'

    if method == 'ping':
        return ping(params, request_id, user_id)
    if method == 'get_result':
        return getResult(params, request_id, user_id)
    # review
    if method == 'answer_review':
        return answerReview(params, request_id, user_id, prompt, companyInfo)
    # post    
    if method == 'scheduled_post':
        return scheduledPost(params, request_id, user_id)
    if method == 'mark_post_as_published':
        return markPostAsPublished(params, request_id, user_id)
    # issue    
    if method == 'existed_issue':
        return existedIssues(params, request_id, user_id)
    if method == 'create_issue':
        return createIssue(params, request_id, user_id)
    if method == 'get_issue':
        return getIssue(params, request_id, user_id)
    if method == 'mark_issue_as_published':
        return markIssueAsPublished(params, request_id, user_id)
    else:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': -32601,
                'message': 'Method not found'
            },
            'id': request_id
        })