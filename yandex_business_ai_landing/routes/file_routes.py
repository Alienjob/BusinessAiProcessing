# routes/file_routes.py

import uuid
import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from yandex_business_ai_landing.model import UserFile, Post
from yandex_business_ai_landing.forms import PhotoUploadForm
from yandex_business_ai_landing.extensions import db, photos

file_routes = Blueprint('file_routes', __name__)

@file_routes.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = PhotoUploadForm()
    if form.validate_on_submit():
        if 'photos' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        files = request.files.getlist('photos')
        if not files or files[0].filename == '':
            flash('No selected files', 'danger')
            return redirect(request.url)
        
        uploaded_files = []
        for file in files:
            if file and photos.file_allowed(file, file.filename):
                original_name = secure_filename(file.filename)
                generated_name = f"{uuid.uuid4().hex}_{original_name}"
                
                try:
                    filename = photos.save(file, name=generated_name)
                    file_url = f"/_uploads/photos/{filename}"
                    
                    file.seek(0, os.SEEK_END)
                    file_size = file.tell()
                    file.seek(0)
                    
                    if file_size > 16 * 1024 * 1024:  # 16 MB limit
                        flash(f'File {original_name} exceeds the size limit of 16 MB and was not uploaded.', 'danger')
                        continue
                    
                    file_type = file.mimetype
                    
                    user_file = UserFile(
                        original_name=original_name,
                        generated_name=generated_name,
                        url=file_url,
                        file_size=file_size,
                        file_type=file_type,
                        user_id=current_user.id
                    )
                    
                    db.session.add(user_file)
                    uploaded_files.append(original_name)
                except Exception as e:
                    flash(f'An error occurred while uploading {original_name}: {str(e)}', 'danger')
                    continue
        
        try:
            db.session.commit()
            if uploaded_files:
                flash(f'Successfully uploaded: {", ".join(uploaded_files)}', 'success')
            return redirect(url_for('file_routes.upload'))
        except Exception as e:
            flash(f'An error occurred while saving files to the database: {str(e)}', 'danger')
            return redirect(request.url)
    
    user_files = current_user.files
    return render_template('upload.html', form=form, files=user_files)

@file_routes.route('/delete_file/<int:id>', methods=['POST'])
@login_required
def delete_file(id):

    user_file = UserFile.query.get_or_404(id)

    associated_posts = Post.query.filter_by(user_file_id=id).all()
    if associated_posts:
        flash('Cannot delete the file. There are associated posts that need to be deleted first.', 'danger')
        return redirect(url_for('file_routes.upload'))

    db.session.delete(user_file)
    db.session.commit()
    flash('File deleted successfully!', 'success')
    return redirect(url_for('file_routes.upload'))