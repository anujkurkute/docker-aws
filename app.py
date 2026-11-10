from flask import Flask, render_template, request, jsonify
import os
from database import init_db
from models import db, Task

app = Flask(__name__)

# Initialize database connection
init_db(app)

@app.route('/')
def index():
    """Main page - serves the frontend"""
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """API endpoint to get all tasks from PostgreSQL database"""
    try:
        # Query all tasks from database
        # SQL equivalent: SELECT * FROM tasks;
        tasks = Task.query.order_by(Task.id.desc()).all()
        
        # Convert Task objects to dictionaries for JSON response
        return jsonify([task.to_dict() for task in tasks])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """API endpoint to create a new task in PostgreSQL database"""
    try:
        data = request.json
        title = data.get('title', '').strip()
        
        if not title:
            return jsonify({"error": "Title is required"}), 400
        
        # Create new Task object
        # SQL equivalent: INSERT INTO tasks (title, completed) VALUES (?, false);
        new_task = Task(title=title, completed=False)
        
        # Add to database session
        db.session.add(new_task)
        
        # Commit transaction (saves to database)
        db.session.commit()
        
        # Return created task
        return jsonify(new_task.to_dict()), 201
    except Exception as e:
        db.session.rollback()  # Undo changes on error
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """API endpoint to update a task in PostgreSQL database"""
    try:
        # Find task by ID
        # SQL equivalent: SELECT * FROM tasks WHERE id = ?;
        task = Task.query.get_or_404(task_id)
        
        data = request.json
        
        # Update task fields if provided
        if 'title' in data:
            task.title = data['title'].strip()
        
        if 'completed' in data:
            task.completed = bool(data['completed'])
        
        # Commit changes to database
        # SQL equivalent: UPDATE tasks SET title=?, completed=? WHERE id=?;
        db.session.commit()
        
        return jsonify(task.to_dict())
    except Exception as e:
        db.session.rollback()
        if '404' in str(e):
            return jsonify({"error": "Task not found"}), 404
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """API endpoint to delete a task from PostgreSQL database"""
    try:
        # Find task by ID
        # SQL equivalent: SELECT * FROM tasks WHERE id = ?;
        task = Task.query.get_or_404(task_id)
        
        # Delete task from database
        # SQL equivalent: DELETE FROM tasks WHERE id = ?;
        db.session.delete(task)
        
        # Commit transaction
        db.session.commit()
        
        return jsonify({"message": "Task deleted"}), 200
    except Exception as e:
        db.session.rollback()
        if '404' in str(e):
            return jsonify({"error": "Task not found"}), 404
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint for Docker"""
    try:
        # Check database connection
        from sqlalchemy import text
        db.session.execute(text("SELECT 1"))
        db_connected = True
    except Exception as e:
        db_connected = False
        print(f"Database connection error: {e}")
    
    return jsonify({
        "status": "healthy" if db_connected else "degraded",
        "service": "flask-app",
        "database": "connected" if db_connected else "disconnected"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

