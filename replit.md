# TaskTracker - Flask Task Management Application

## Overview
TaskTracker is a comprehensive task management web application built with Flask and SQLAlchemy. It enables teams to create, assign, and track tasks with features like user management, task filtering, and progress monitoring. The application follows a traditional MVC pattern with Flask as the web framework, SQLAlchemy for data persistence, and Bootstrap for the frontend interface.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with Blueprint-style routing
- **ORM**: SQLAlchemy with DeclarativeBase for database operations
- **Database**: SQLite (default) with configurable PostgreSQL support
- **Forms**: Flask-WTF for form handling and validation
- **Session Management**: Flask's built-in session handling with configurable secret key

### Frontend Architecture
- **Template Engine**: Jinja2 templates with base template inheritance
- **CSS Framework**: Bootstrap 5 with dark theme
- **Icons**: Font Awesome 6.0
- **JavaScript**: Bootstrap's built-in JavaScript components
- **Responsive Design**: Mobile-first approach using Bootstrap's grid system

### Database Schema
The application uses a relational database with two main entities:
- **Users Table**: id, name, email, role, created_at
- **Tasks Table**: id, title, description, status, priority, due_date, created_at, updated_at
- **Many-to-Many Relationship**: task_assignments table linking users to tasks

## Key Components

### Models (models.py)
- **User Model**: Represents team members with roles (Member, Manager, Admin)
- **Task Model**: Represents tasks with status tracking and priority levels
- **Association Table**: Handles many-to-many relationships between users and tasks

### Services (services.py)
- **TaskService**: Handles CRUD operations, filtering, and business logic for tasks
- **UserService**: Manages user-related operations and statistics

### Forms (forms.py)
- **TaskForm**: Multi-field form with custom checkbox widget for user assignment
- **UserForm**: Simple form for user creation and editing
- **TaskFilterForm**: Dynamic filtering form with database-populated choices

### Routes (routes.py)
- **Dashboard Route**: Statistics and overview page
- **Task Routes**: CRUD operations and filtering
- **User Routes**: User management endpoints

## Data Flow

1. **Request Processing**: Flask receives HTTP requests and routes them to appropriate view functions
2. **Form Handling**: Flask-WTF validates and processes form data
3. **Service Layer**: Business logic is handled in service classes
4. **Database Operations**: SQLAlchemy ORM manages database transactions
5. **Template Rendering**: Jinja2 renders HTML with context data
6. **Response**: Flask returns rendered templates or redirects

### Task Assignment Flow
- Users can be assigned to multiple tasks through a many-to-many relationship
- Assignment updates are handled atomically with rollback on errors
- Task filtering supports filtering by assigned users

## External Dependencies

### Python Packages
- **Flask**: Web framework and core functionality
- **Flask-SQLAlchemy**: ORM integration
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form validation and rendering
- **Werkzeug**: WSGI utilities and ProxyFix middleware

### Frontend Dependencies (CDN)
- **Bootstrap 5**: CSS framework with dark theme variant
- **Font Awesome 6**: Icon library

### Environment Variables
- **DATABASE_URL**: Database connection string (defaults to SQLite)
- **SESSION_SECRET**: Flask session encryption key

## Deployment Strategy

### Development Configuration
- **Database**: SQLite file-based database (tasktracker.db)
- **Debug Mode**: Enabled for development
- **Host/Port**: Configurable (default: 0.0.0.0:5000)

### Production Considerations
- **Database**: Configurable to PostgreSQL via DATABASE_URL environment variable
- **Session Security**: Custom secret key via SESSION_SECRET environment variable
- **Proxy Support**: ProxyFix middleware for reverse proxy deployments
- **Connection Pooling**: Configured with pool_recycle and pool_pre_ping for stability

### Database Initialization
- **Auto-creation**: Tables are created automatically on application startup
- **Migration Strategy**: Uses SQLAlchemy's create_all() method (suitable for development)

The application is designed to be easily deployable on platforms like Replit, Heroku, or similar PaaS providers with minimal configuration changes.