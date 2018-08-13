from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo , ValidationError
from todo import db
from todo.models import Task, Subtask

class AddTask(FlaskForm):

    Title = StringField('Title',
                           validators=[DataRequired(), Length(min=2, max=20)])
    Description = StringField('Description',
                           validators=[DataRequired(), Length(min=2, max=20)])
    DueDate = StringField('DueDate',
                           validators=[DataRequired(), Length(min=2, max=20)])
    Status = BooleanField('Open Status' , default= True)

    submit = SubmitField('Add')
    
    def validate_Title(self, Title):
        title = Task.query.filter_by(Title=title.data).first()
        if title:
            raise ValidationError('That Title is taken. Please choose a different one.')

    def validate_DueDate(self,DueDate):
        print("working")