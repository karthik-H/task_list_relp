# TaskTracker

A comprehensive task tracking web application built with Flask and SQLAlchemy that allows teams to manage tasks, assign users, and track progress efficiently.

## Features

### Task Management
- **CRUD Operations**: Create, read, update, and delete tasks
- **Task Properties**: Each task includes:
  - Unique ID
  - Title and description
  - Status (To Do, In Progress, Done)
  - Priority levels (Low, Medium, High)
  - Due dates with overdue indicators
  - Creation and update timestamps

### User Management
- **User CRUD**: Add, edit, and delete team members
- **User Properties**: Each user has:
  - Unique ID
  - Name and email
  - Role (Member, Manager, Admin)
  - Creation timestamp

### Task Assignment
- **Multi-user Assignment**: Assign multiple users to a single task
- **Easy Reassignment**: Update task assignees without deleting the task
- **Assignment Tracking**: View which users are assigned to which tasks

### Filtering & Views
- **Filter Tasks By**:
  - Assigned user
  - Task status
  - Priority level
  - Due date
- **Dashboard Overview**: Statistics and recent tasks
- **Responsive Design**: Works on desktop and mobile devices

### Additional Features
- **Overdue Detection**: Visual indicators for overdue tasks
- **Form Validation**: Client and server-side validation
- **Error Handling**: User-friendly error messages
- **Dark Theme**: Modern Bootstrap dark theme interface

## Technology Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Database (configurable to PostgreSQL)
- **Flask-WTF**: Form handling and validation
- **Python-dateutil**: Date handling utilities

### Frontend
- **HTML5 & Jinja2**: Template engine
- **Bootstrap 5**: Responsive CSS framework with dark theme
- **Font Awesome**: Icons
- **Vanilla JavaScript**: Client-side interactivity

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Environment Setup
1. **Clone or download the project files**

2. **Set environment variables**:
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   export DATABASE_URL="sqlite:///tasktracker.db"  # Optional, defaults to SQLite
   