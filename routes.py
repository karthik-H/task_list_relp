from flask import render_template, request, redirect, url_for, flash
from app import app
from forms import TaskForm, UserForm, TaskFilterForm
from services import TaskService, UserService
from models import Task, User

@app.route('/')
def index():
    """Dashboard with overview statistics"""
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status='Done').count()
    in_progress_tasks = Task.query.filter_by(status='In Progress').count()
    from datetime import datetime
    overdue_tasks = Task.query.filter(
        Task.due_date < datetime.utcnow(),
        Task.status != 'Done'
    ).count()
    
    recent_tasks = Task.query.order_by(Task.created_at.desc()).limit(5).all()
    user_stats = UserService.get_user_statistics()
    
    return render_template('index.html',
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         in_progress_tasks=in_progress_tasks,
                         overdue_tasks=overdue_tasks,
                         recent_tasks=recent_tasks,
                         user_stats=user_stats)

@app.route('/tasks')
def tasks():
    """View all tasks with filtering"""
    filter_form = TaskFilterForm(request.args)
    
    if filter_form.validate():
        # Apply filters
        assignee_id = filter_form.assignee.data if filter_form.assignee.data else None
        status = filter_form.status.data if filter_form.status.data else None
        priority = filter_form.priority.data if filter_form.priority.data else None
        
        tasks = TaskService.filter_tasks(assignee_id, status, priority)
    else:
        tasks = TaskService.get_all_tasks()
    
    return render_template('tasks.html', tasks=tasks, filter_form=filter_form)

@app.route('/tasks/new', methods=['GET', 'POST'])
def new_task():
    """Create a new task"""
    form = TaskForm()
    
    if form.validate_on_submit():
        task, error = TaskService.create_task(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            assignee_ids=form.assignees.data
        )
        
        if task:
            flash(f'Task "{task.title}" created successfully!', 'success')
            return redirect(url_for('tasks'))
        else:
            flash(f'Error creating task: {error}', 'danger')
    
    return render_template('task_form.html', form=form, title='Create New Task')

@app.route('/tasks/<int:task_id>')
def task_detail(task_id):
    """View task details"""
    task = TaskService.get_task_by_id(task_id)
    return render_template('task_detail.html', task=task)

@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    """Edit an existing task"""
    task = TaskService.get_task_by_id(task_id)
    form = TaskForm(obj=task)
    
    # Pre-populate assignees
    if request.method == 'GET':
        form.assignees.data = [user.id for user in task.assignees]
    
    if form.validate_on_submit():
        updated_task, error = TaskService.update_task(
            task_id=task_id,
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            assignee_ids=form.assignees.data
        )
        
        if updated_task:
            flash(f'Task "{updated_task.title}" updated successfully!', 'success')
            return redirect(url_for('task_detail', task_id=task_id))
        else:
            flash(f'Error updating task: {error}', 'danger')
    
    return render_template('task_form.html', form=form, task=task, title='Edit Task')

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """Delete a task"""
    success, error = TaskService.delete_task(task_id)
    
    if success:
        flash('Task deleted successfully!', 'success')
    else:
        flash(f'Error deleting task: {error}', 'danger')
    
    return redirect(url_for('tasks'))

@app.route('/users')
def users():
    """View all users"""
    users = UserService.get_all_users()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    """Create a new user"""
    form = UserForm()
    
    if form.validate_on_submit():
        user, error = UserService.create_user(
            name=form.name.data,
            email=form.email.data,
            role=form.role.data
        )
        
        if user:
            flash(f'User "{user.name}" created successfully!', 'success')
            return redirect(url_for('users'))
        else:
            flash(f'Error creating user: {error}', 'danger')
    
    return render_template('user_form.html', form=form, title='Create New User')

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit an existing user"""
    user = UserService.get_user_by_id(user_id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        updated_user, error = UserService.update_user(
            user_id=user_id,
            name=form.name.data,
            email=form.email.data,
            role=form.role.data
        )
        
        if updated_user:
            flash(f'User "{updated_user.name}" updated successfully!', 'success')
            return redirect(url_for('users'))
        else:
            flash(f'Error updating user: {error}', 'danger')
    
    return render_template('user_form.html', form=form, user=user, title='Edit User')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""
    success, error = UserService.delete_user(user_id)
    
    if success:
        flash('User deleted successfully!', 'success')
    else:
        flash(f'Error deleting user: {error}', 'danger')
    
    return redirect(url_for('users'))
