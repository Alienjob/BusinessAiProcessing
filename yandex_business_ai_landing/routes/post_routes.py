# routes/post_routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from yandex_business_ai_landing.model import UserFile, Post, LongOperation, UserPrompts, User
from yandex_business_ai_landing.llm.generate_image_description import generateImageDescription
from yandex_business_ai_landing.llm.write_topic import generatePostContent
import time
from datetime import datetime
from yandex_business_ai_landing.extensions import db
import logging

post_routes = Blueprint('post_routes', __name__)

@post_routes.route('/control_posts', methods=['GET', 'POST'])
@login_required
def control_posts():

    if request.method == 'POST':
        file_id = request.form.get('file_id')
        post_id = request.form.get('post_id')
        post_content = request.form.get('post_content')
        photo_description = request.form.get('photo_description')
        posting_time_str = request.form.get('posting_time')
        status = request.form.get('status')

        user_file = UserFile.query.get_or_404(file_id)
        
        # Convert the posting_time string to a datetime object
        posting_time = datetime.strptime(posting_time_str, '%Y-%m-%dT%H:%M') if posting_time_str else None
        
        if post_id:
            post = Post.query.get_or_404(post_id)
            post.post_content = post_content
            post.photo_description = photo_description
            post.posting_time = posting_time
            post.status = status
            db.session.commit()
            flash('Post updated successfully!', 'success')
        else:
            new_post = Post(
                photo_url=user_file.url,
                post_content=post_content,
                photo_description=photo_description,
                posting_time=posting_time,
                status=status,
                user_id=current_user.id,
                user_file_id=user_file.id
            )
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
        
        return redirect(url_for('post_routes.control_posts'))

    filter_status = request.args.get('filter_status')
    sort_by_status = request.args.get('sort_by_status', 'off')
    sort_by_publishing_time = request.args.get('sort_by_publishing_time', 'off')

    query = UserFile.query.filter_by(user_id=current_user.id).outerjoin(Post, UserFile.id == Post.user_file_id)

    if filter_status == 'no_posts':
        query = query.filter(Post.id.is_(None))
    elif filter_status in ['draft', 'published']:
        query = query.filter(Post.status == filter_status)

    if sort_by_status == 'on':
        query = query.order_by(Post.status.asc().nullslast(), UserFile.upload_time.desc())
    elif sort_by_publishing_time == 'on':
        query = query.order_by(Post.posting_time.desc().nullslast(), UserFile.upload_time.desc())
    else:
        query = query.order_by(UserFile.upload_time.desc())

    # Log the resulting SQL query
    logging.info(str(query))

    user_files = query.all()
    return render_template('control_posts.html', 
                         files=user_files, 
                         filter_status=filter_status, 
                         sort_by_status=sort_by_status,
                         sort_by_publishing_time=sort_by_publishing_time)

@post_routes.route('/create_post', methods=['POST'])
@login_required
def create_post():
    file_id = request.form.get('file_id')
    user_file = UserFile.query.get_or_404(file_id)
    
    new_post = Post(
        photo_url=user_file.url,
        post_content='',
        photo_description='',
        posting_time=None,
        user_id=current_user.id,
        user_file_id=user_file.id
    )
    db.session.add(new_post)
    db.session.commit()
    flash('Post created successfully!', 'success')
    return redirect(url_for('post_routes.control_posts'))

@post_routes.route('/generate_description/<int:file_id>', methods=['POST'])
@login_required
def generate_description(file_id):
    user_file = UserFile.query.get_or_404(file_id)
    params = [{'name': 'image_url', 'value': user_file.url}]
    request_id = request.json.get('id')
    user_id = current_user.id

    userPrompts = UserPrompts.query.filter_by(user_id=user_id).first()
    prompt = userPrompts.describe_picture_prompt if userPrompts else None

    user = User.query.get(user_id)
    if user is None:
        companyInfo = 'Информация о компании не заполнена'
    else:
        company_name = user.company_name if user.company_name else 'Название компании не указано'
        company_description = user.company_description if user.company_description else 'Описание компании не указано'
        additional_info = user.additional_info if user.additional_info else 'Дополнительная информация не указана'
        companyInfo = f'Название компании: {company_name}\nОписание компании: {company_description}\nДополнительная информация: {additional_info}'
   

    # Start the generation process
    response = generateImageDescription(params, request_id, user_id, prompt, companyInfo)
    operation_id = response.json['result']['id']

    # ensure that the operation_id is a valid integer
    operation_id = int(operation_id)
    
    operation = LongOperation.query.get(operation_id)
    
    result = operation.json()

    # Return the final result
    return result
    
    
@post_routes.route('/generate_post_content/<int:file_id>', methods=['POST'])
@login_required
def generate_post_content(file_id):

    image_description = request.json.get('image_description')
    user_file = UserFile.query.get_or_404(file_id)

    params = [{'name': 'image_url', 'value': user_file.url},
              {'name': 'image_description', 'value': image_description}]
    request_id = request.json.get('id')
    user_id = current_user.id

    userPrompts = UserPrompts.query.filter_by(user_id=user_id).first()
    prompt = userPrompts.write_article_prompt if userPrompts else None

    user = User.query.get(user_id)
    if user is None:
        companyInfo = 'Информация о компании не заполнена'
    else:
        company_name = user.company_name if user.company_name else 'Название компании не указано'
        company_description = user.company_description if user.company_description else 'Описание компании не указано'
        additional_info = user.additional_info if user.additional_info else 'Дополнительная информация не указана'
        companyInfo = f'Название компании: {company_name}\nОписание компании: {company_description}\nДополнительная информация: {additional_info}'

    # Start the generation process
    response = generatePostContent(params, request_id, user_id, prompt, companyInfo, image_description)
    operation_id = response.json['result']['id']

    operation = LongOperation.query.get(operation_id)

    result = operation.json()

    # Return the final result
    return result

@post_routes.route('/operation_result/<int:operation_id>', methods=['GET'])
@login_required
def operation_result(operation_id):
    operation = LongOperation.query.get_or_404(operation_id)
    return jsonify(operation.json())

@post_routes.route('/delete_post/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('post_routes.control_posts'))

@post_routes.route('/delete_image/<int:id>', methods=['POST'])
@login_required
def delete_image(id):
    user_file = UserFile.query.get_or_404(id)
    
    # Delete all posts associated with this image
    posts = Post.query.filter_by(user_file_id=id).all()
    for post in posts:
        db.session.delete(post)
    
    db.session.delete(user_file)
    db.session.commit()
    flash('Image and associated posts deleted successfully!', 'success')
    return redirect(url_for('post_routes.control_posts'))