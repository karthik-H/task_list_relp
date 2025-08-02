from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

# Association table for many-to-many relationship between tasks and users
task_assignments = Table(
    'task_assignments',
    db.Model.metadata,
    Column('task_id', Integer, ForeignKey('task.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True)
)

class User(db.Model):
    """User model for storing user information"""
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    role = Column(String(50), nullable=False, default='Member')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to tasks assigned to this user
    assigned_tasks = relationship('Task', secondary=task_assignments, back_populates='assignees')
    
    def __repr__(self):
        return f'<User {self.name}>'

class Task(db.Model):
    """Task model for storing task information"""
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(20), nullable=False, default='To Do')  # To Do, In Progress, Done
    priority = Column(String(10), nullable=False, default='Medium')  # Low, Medium, High
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to users assigned to this task
    assignees = relationship('User', secondary=task_assignments, back_populates='assigned_tasks')
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    @property
    def status_class(self):
        """Return CSS class for status"""
        status_classes = {
            'To Do': 'secondary',
            'In Progress': 'warning',
            'Done': 'success'
        }
        return status_classes.get(self.status, 'secondary')
    
    @property
    def priority_class(self):
        """Return CSS class for priority"""
        priority_classes = {
            'Low': 'success',
            'Medium': 'warning',
            'High': 'danger'
        }
        return priority_classes.get(self.priority, 'secondary')
    
    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and self.status != 'Done':
            return datetime.utcnow() > self.due_date
        return False
