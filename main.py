from fastapi import FastAPI, Path, Query, HTTPException
from model import db, Task 
from pydantic import BaseModel, Field
from typing import Annotated, Literal

app = FastAPI()

class Task_class(BaseModel):
    title: Annotated[str, Field(..., description="enter the task you want to achieve today",examples=["Drink water"])]
    status: Annotated[Literal["Done","Not Done"], Field(...,description="Click done after the task is performed.")]

@app.get("/")
def hello():
    return {"message": "Hello"}

@app.get("/task/all")
def get_task_all():
    tasks = Task.query.all()
    res=[]
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    for task in tasks:
        res.append(
            {
            "title": task.title,
            "status": task.status
            }
        )
    return(res)

@app.get("/task/{task_id}")
def get_task_id(task_id: int = Path(..., description="ID of the task you want to view", example=1)):
    task = Task.query.filter_by(task_id = task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return ({
        "title": task.title,
        "status": task.status
    })

@app.get("/sort")
def task_sort(sort_by: str= Query(..., description="Sort by Task is finished or not finished"), order: str=Query()):
    return(sorted_data)

@app.post("/create/task")
def create_task(data: Task_class):
    task = Task(title = data.title)
    db.session.add(task)
    db.session.commit()