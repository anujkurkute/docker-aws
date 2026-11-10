
import os

# Use an isolated SQLite database for automated tests.
os.environ["DATABASE_URL"] = "sqlite://"

from app import app
from models import db


def setup_function():
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()


def teardown_function():
    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_health():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.json["database"] == "connected"


def test_get_tasks():
    response = app.test_client().get("/api/tasks")

    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_create_task():
    response = app.test_client().post(
        "/api/tasks",
        json={"title": "CI/CD deployment test"}
    )

    assert response.status_code == 201
    assert response.json["title"] == "CI/CD deployment test"


def test_create_task_without_title():
    response = app.test_client().post(
        "/api/tasks",
        json={"title": ""}
    )

    assert response.status_code == 400


def test_update_and_delete_task():
    client = app.test_client()

    create_response = client.post(
        "/api/tasks",
        json={"title": "Test task"}
    )

    task_id = create_response.json["id"]

    update_response = client.put(
        f"/api/tasks/{task_id}",
        json={"completed": True}
    )

    assert update_response.status_code == 200
    assert update_response.json["completed"] is True

    delete_response = client.delete(f"/api/tasks/{task_id}")

    assert delete_response.status_code == 200
