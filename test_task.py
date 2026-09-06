import pytest
from fastapi.testclient import TestClient
from main import app

Client = TestClient(app)

def test_create_task():
    response = Client.post("/create/task", json={"title":"test task", "status":False})
    assert response.status_code == 201
    assert "message" in response.json()

def test_get_all_tasks():
    response = Client.get("/view")
    assert response.status_code == 200
    assert isinstance(response.json(),dict)

def test_task_that_does_not_exist():
    response = Client.get("/task/12345678")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_delete_task():
    create_response = Client.post("/create/task", json = {"title": "haha find me","status" : True})
    task_id = list(Client.get("/view").json().keys())[-1]
    response = Client.delete(f"/delete/{task_id}")
    assert response.status_code == 200
    assert "message" in response.json()

def test_update_task():
    create_task = Client.post("/create/task", json = {"title": "haha find me","status" : True})
    task_id = list(Client.get("/view").json().keys())[-1]
    response = Client.put(f"/edit/{task_id}", json={"title" : "hhaa new me"})
    assert response.status_code == 200
    assert "message" in response.json()

def test_individual_task():
    task_id = list(Client.get("/view").json().keys())[-1]
    response = Client.get(f"/task/{task_id}")
    assert response.status_code == 200


def test_filter_task():
    response = Client.get("/filter?order=finished")
    assert response.json()[0][1]["status"] == True

def test_filter_task2():
    response = Client.get("/filter?order=not finished")
    assert response.json()[0][1]["status"] == False