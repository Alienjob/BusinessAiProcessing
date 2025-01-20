from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from yandex_business_ai_landing.extensions import db

personal_cabinet_routes = Blueprint('personal_cabinet_routes', __name__)

@personal_cabinet_routes.route('/personal_cabinet')
@login_required
def personal_cabinet():
    return render_template('personal_cabinet.html', user=current_user)

@personal_cabinet_routes.route('/update_personal_cabinet', methods=['POST'])
@login_required
def update_personal_cabinet():
    current_user.company_name = request.form.get('company_name')
    current_user.company_description = request.form.get('company_description')
    current_user.additional_info = request.form.get('additional_info')
    db.session.commit()
    return redirect(url_for('personal_cabinet_routes.personal_cabinet'))

@personal_cabinet_routes.route('/long_operations')
@login_required
def long_operations():
    return render_template('long_operations.html')

@personal_cabinet_routes.route('/test_long_operations')
@login_required
def test_long_operations():
    return render_template('test_long_operations.html')