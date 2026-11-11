"""
Database Models for the Task Manager Application

This file defines the database schema using SQLAlchemy ORM.
ORM = Object-Relational Mapping (Python objects represent database tables)
"""

from flask_sqlalchemy import SQLAlchemy

# Create database instance
# This will be initialized in app.py
db = SQLAlchemy()


class Task(db.Model):
    """
    Task Model - Represents a task in the database
    
    This class maps to a 'tasks' table in PostgreSQL.
    Each Task object represents one row in the table.
    """
    
    # Table name (defaults to lowercase class name + 's')
    __tablename__ = 'tasks'
    
    # Column definitions (each = one database column)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """
    id - Primary key (unique identifier for each task)
    - Integer type
    - Primary key = unique, auto-incrementing
    - Every task has a unique ID
    """
    
    title = db.Column(db.String(200), nullable=False)
    """
    title - Task title/description
    - String type, max 200 characters
    - nullable=False means this field is required
    """
    
    completed = db.Column(db.Boolean, default=False, nullable=False)
    """
    completed - Whether task is done or not
    - Boolean type (True/False)
    - Default value = False (tasks start as incomplete)
    - nullable=False means this field is required
    """
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    """
    created_at - Timestamp when task was created
    - DateTime type
    - server_default=db.func.now() sets current time automatically
    - PostgreSQL will set this when inserting a new row
    """
    
    def to_dict(self):
        """
        Convert Task object to dictionary (for JSON API responses)
        This makes it easy to send data to frontend
        """
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        """
        String representation of Task object (for debugging)
        Example: <Task 1: Learn Docker>
        """
        return f'<Task {self.id}: {self.title}>'

