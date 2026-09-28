import pytest
from fastapi.testclient import TestClient
from main import app, TaskRequest, process_task

client = TestClient(app)

def test_startup():
    assert app.title == "Diff Builder MVP"

def test_happy_path():
    response = client.post("/task", json={
        "query": "change missing to present",
        "files": {"main.py": "print('hello')"}
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert len(data["diffs"]) == 1
    assert data["diffs"][0]["action"] == "replace"

def test_failure_path():
    response = client.post("/task", json={
        "query": "invalid",
        "files": {} 
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert len(data["diffs"]) == 0
