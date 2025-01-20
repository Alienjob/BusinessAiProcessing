# forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from wtforms.validators import DataRequired

class PhotoUploadForm(FlaskForm):
    photos = FileField('Upload Photos', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ], render_kw={"multiple": True})
    submit = SubmitField('Upload')