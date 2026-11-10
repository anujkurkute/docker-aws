
from app import app
from models import db, Task

with app.app_context():
    db.create_all()

    if Task.query.count() == 0:
        sample_tasks = [
            Task(title="Learn Docker", completed=False),
            Task(title="Learn PostgreSQL", completed=False),
            Task(title="Build Flask App with Database", completed=False)
        ]

        db.session.add_all(sample_tasks)
        db.session.commit()

    print("Database initialization completed successfully!")
