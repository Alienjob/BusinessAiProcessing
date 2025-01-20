from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from yandex_business_ai_landing.model import UserPrompts
from yandex_business_ai_landing.api.answer_review import answerReviewSystemPrompt
from yandex_business_ai_landing.llm.generate_image_description import generateImageDescriptionSystemPrompt
from yandex_business_ai_landing.llm.write_topic import writeTopicSystemPrompt
from yandex_business_ai_landing.llm.write_issue_response import writeIssueResponseSystemPrompt
from yandex_business_ai_landing.extensions import db

user_prompts_routes = Blueprint('user_prompts_routes', __name__)

@user_prompts_routes.route('/edit_prompts', methods=['GET', 'POST'])
@login_required
def edit_prompts():
    prompts = UserPrompts.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        review_prompt = request.form.get('review_prompt')
        describe_picture_prompt = request.form.get('describe_picture_prompt')
        write_article_prompt = request.form.get('write_article_prompt')
        write_issue_response_prompt = request.form.get('write_issue_response_prompt')

        if not prompts:
            prompts = UserPrompts(
                user_id=current_user.id,
                review_prompt=review_prompt,
                describe_picture_prompt=describe_picture_prompt,
                write_article_prompt=write_article_prompt,
                write_issue_response_prompt=write_issue_response_prompt
            )
            db.session.add(prompts)
        else:
            prompts.review_prompt = review_prompt
            prompts.describe_picture_prompt = describe_picture_prompt
            prompts.write_article_prompt = write_article_prompt
            prompts.write_issue_response_prompt = write_issue_response_prompt

        db.session.commit()
        flash('Prompts updated successfully!', 'success')
        return redirect(url_for('user_prompts_routes.edit_prompts'))

    return render_template('edit_prompts.html', 
                           prompts=prompts, 
                           answer_review_system_prompt=answerReviewSystemPrompt, 
                           generate_image_description_system_prompt=generateImageDescriptionSystemPrompt,
                           write_article_system_prompt=writeTopicSystemPrompt,
                           write_issue_response_system_prompt=writeIssueResponseSystemPrompt)