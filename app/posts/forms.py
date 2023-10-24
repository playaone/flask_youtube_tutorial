from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired

# =======================================================================================================================

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=4, max=120)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=300)])
    tags = StringField('Tags', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Post Content', validators=[DataRequired(), Length(min=10)])
    image_file = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')
    
    