from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeLocalField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import CheckboxInput, ListWidget
from models import User

class MultiCheckboxField(SelectMultipleField):
    """Custom field for multiple checkboxes"""
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class TaskForm(FlaskForm):
    """Form for creating and editing tasks"""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    status = SelectField('Status', 
                        choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done')],
                        default='To Do')
    priority = SelectField('Priority',
                         choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')],
                         default='Medium')
    due_date = DateTimeLocalField('Due Date', format='%Y-%m-%dT%H:%M')
    assignees = MultiCheckboxField('Assignees', coerce=int)
    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # Populate assignees choices from database
        self.assignees.choices = [(user.id, user.name) for user in User.query.all()]

class UserForm(FlaskForm):
    """Form for creating and editing users"""
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    role = SelectField('Role',
                      choices=[('Member', 'Member'), ('Manager', 'Manager'), ('Admin', 'Admin')],
                      default='Member')

class TaskFilterForm(FlaskForm):
    """Form for filtering tasks"""
    assignee = SelectField('Assignee', coerce=int)
    status = SelectField('Status')
    priority = SelectField('Priority')
    
    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        
        # Populate assignee choices
        users = User.query.all()
        self.assignee.choices = [('', 'All Users')] + [(user.id, user.name) for user in users]
        
        # Status choices
        self.status.choices = [('', 'All Status'), ('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done')]
        
        # Priority choices
        self.priority.choices = [('', 'All Priorities'), ('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]
