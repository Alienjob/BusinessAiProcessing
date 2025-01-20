from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from yandex_business_ai_landing.model import ReviewIssue, LongOperation, UserPrompts, User
from yandex_business_ai_landing.extensions import db, executor
from yandex_business_ai_landing.llm.write_issue_response import writeIssueResponse
import json

review_routes = Blueprint('review_routes', __name__)

@review_routes.route('/review_issues', methods=['GET'])
@login_required
def review_issues():
    review_issues = ReviewIssue.query.filter_by(user_id=current_user.id).all()
    return render_template('review_issue.html', review_issues=review_issues)

@review_routes.route('/add_review_issue', methods=['POST'])
@login_required
def add_review_issue():
    review_rate = request.form.get('review_rate')
    review_text = request.form.get('review_text')
    company_story = request.form.get('company_story')
    company_response = request.form.get('company_response')
    status = request.form.get('status')

    new_review_issue = ReviewIssue(
        user_id=current_user.id,
        review_rate=review_rate,
        review_text=review_text,
        company_story=company_story,
        company_response=company_response,
        status=status
    )
    db.session.add(new_review_issue)
    db.session.commit()
    flash('Review issue added successfully!', 'success')
    return redirect(url_for('review_routes.review_issues'))

@review_routes.route('/update_review_issue/<int:id>', methods=['POST'])
@login_required
def update_review_issue(id):
    review_issue = ReviewIssue.query.get_or_404(id)
    review_issue.review_rate = request.form.get('review_rate')
    review_issue.review_text = request.form.get('review_text')
    review_issue.company_story = request.form.get('company_story')
    review_issue.company_response = request.form.get('company_response')
    review_issue.status = request.form.get('status')

    db.session.commit()
    flash('Review issue updated successfully!', 'success')
    return redirect(url_for('review_routes.review_issues'))

@review_routes.route('/delete_review_issue/<int:id>', methods=['POST'])
@login_required
def delete_review_issue(id):
    review_issue = ReviewIssue.query.get_or_404(id)
    db.session.delete(review_issue)
    db.session.commit()
    flash('Review issue deleted successfully!', 'success')
    return redirect(url_for('review_routes.review_issues'))

@review_routes.route('/generate_issue_response/<int:issue_id>', methods=['POST'])
@login_required
def generate_issue_response(issue_id):
    review_issue = ReviewIssue.query.get_or_404(issue_id)
    request_id = request.json.get('id')
    
    review_text = request.json.get('review_text')
    company_story = request.json.get('company_story')
    
    params = [
        {
            'name': 'review_text', 
            'value': review_text
        },
        {
            'name': 'company_story',
            'value': company_story
        }
    ]

    user_id = current_user.id

    userPrompts = UserPrompts.query.filter_by(user_id=user_id).first()
    prompt = userPrompts.write_issue_response_prompt if userPrompts else None

    user = User.query.get(user_id)
    if user is None:
        companyInfo = 'Информация о компании не заполнена'
    else:
        company_name = user.company_name if user.company_name else 'Название компании не указано'
        company_description = user.company_description if user.company_description else 'Описание компании не указано'
        additional_info = user.additional_info if user.additional_info else 'Дополнительная информация не указана'
        companyInfo = f'Название компании: {company_name}\nОписание компании: {company_description}\nДополнительная информация: {additional_info}'

    # Start the generation process
    
    response = writeIssueResponse(params, request_id, user_id, prompt, review_text, companyInfo, company_story)
    operation_id = response.json['result']['id']

    # ensure that the operation_id is a valid integer
    operation_id = int(operation_id)
    
    operation = LongOperation.query.get(operation_id)
    
    result = operation.json()

    # Return the final result
    return result

@review_routes.route('/operation_result/<int:operation_id>', methods=['GET'])
@login_required
def operation_result(operation_id):
    operation = LongOperation.query.get_or_404(operation_id)
    return jsonify(operation.json())

