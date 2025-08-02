from app import db
from models import Task, User
from datetime import datetime
from sqlalchemy import or_, and_

class TaskService:
    """Service class for task-related operations"""
    
    @staticmethod
    def get_all_tasks():
        """Get all tasks ordered by creation date"""
        return Task.query.order_by(Task.created_at.desc()).all()
    
    @staticmethod
    def get_task_by_id(task_id):
        """Get task by ID"""
        return Task.query.get_or_404(task_id)
    
    @staticmethod
    def create_task(title, description, status, priority, due_date, assignee_ids):
        """Create a new task"""
        try:
            task = Task(
                title=title,
                description=description,
                status=status,
                priority=priority,
                due_date=due_date
            )
            
            # Add assignees
            if assignee_ids:
                assignees = User.query.filter(User.id.in_(assignee_ids)).all()
                task.assignees = assignees
            
            db.session.add(task)
            db.session.commit()
            return task, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_task(task_id, title, description, status, priority, due_date, assignee_ids):
        """Update an existing task"""
        try:
            task = Task.query.get_or_404(task_id)
            task.title = title
            task.description = description
            task.status = status
            task.priority = priority
            task.due_date = due_date
            task.updated_at = datetime.utcnow()
            
            # Update assignees
            if assignee_ids:
                assignees = User.query.filter(User.id.in_(assignee_ids)).all()
                task.assignees = assignees
            else:
                task.assignees = []
            
            db.session.commit()
            return task, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def delete_task(task_id):
        """Delete a task"""
        try:
            task = Task.query.get_or_404(task_id)
            db.session.delete(task)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def filter_tasks(assignee_id=None, status=None, priority=None):
        """Filter tasks based on criteria"""
        query = Task.query
        
        if assignee_id:
            query = query.filter(Task.assignees.any(User.id == assignee_id))
        
        if status:
            query = query.filter(Task.status == status)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        return query.order_by(Task.created_at.desc()).all()

class UserService:
    """Service class for user-related operations"""
    
    @staticmethod
    def get_all_users():
        """Get all users ordered by name"""
        return User.query.order_by(User.name).all()
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return User.query.get_or_404(user_id)
    
    @staticmethod
    def create_user(name, email, role):
        """Create a new user"""
        try:
            # Check if email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return None, "Email already exists"
            
            user = User(name=name, email=email, role=role)
            db.session.add(user)
            db.session.commit()
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_user(user_id, name, email, role):
        """Update an existing user"""
        try:
            user = User.query.get_or_404(user_id)
            
            # Check if email already exists for another user
            existing_user = User.query.filter(User.email == email, User.id != user_id).first()
            if existing_user:
                return None, "Email already exists"
            
            user.name = name
            user.email = email
            user.role = role
            db.session.commit()
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def delete_user(user_id):
        """Delete a user"""
        try:
            user = User.query.get_or_404(user_id)
            
            # Check if user has assigned tasks
            if user.assigned_tasks:
                return False, "Cannot delete user with assigned tasks"
            
            db.session.delete(user)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_user_statistics():
        """Get user statistics"""
        total_users = User.query.count()
        users_with_tasks = User.query.join(User.assigned_tasks).distinct().count()
        return {
            'total_users': total_users,
            'users_with_tasks': users_with_tasks,
            'users_without_tasks': total_users - users_with_tasks
        }
