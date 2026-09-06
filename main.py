from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse 
from pydantic import BaseModel, Field
from typing import Annotated, Literal, Optional
import json
import uuid

app = FastAPI()

class Task_class(BaseModel):
    task_id:Optional[str]
    title: Optional[str]
    status: bool = False

class Task_create(BaseModel):
    title:Annotated[str, Field(...,description="Write the task", examples=['Go to gym'])]
    status: bool = False

def load_data():
    with open('task.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('task.json','w') as f:
        json.dump(data,f)

@app.get("/")
def hello():
    return "Welcome to the new start"

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/task/{task_id}")
def get_task_id(task_id: str = Path(..., description="ID of the task you want to view", examples=1)):
    data = load_data()
    if task_id in data:
        return data[task_id]
    raise HTTPException(status_code=404, detail="Task not found")
    
@app.get("/filter")
def task_sort(order: str= Query(..., description="Sort by Task is finished or not finished")):
    valid_fields = ["finished", "not finished"]
    if order not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid field!")
    
    data = load_data()
    
    if order == "finished":
        reverse_status = True
    else:
        reverse_status = False
    return sorted(data.items(), key=lambda x: x[1]["status"], reverse=reverse_status)

@app.post("/create/task")
def create_task(task: Task_create):
    data = load_data()
    task_id = str(uuid.uuid4())
    data[task_id] = task.model_dump()  
    save_data(data)
    return JSONResponse(status_code = 201, content={"message" : "task created succesfully"})

@app.put("/edit/{task_id}")
def update_task(task_id: str, updated_task: Task_create):
    data = load_data()

    if task_id not in data:
        raise HTTPException(404, detail="Task not found")
    
    existing_task = data[task_id]

    updated_task_info = updated_task.model_dump(exclude_unset=True, exclude={"task_id"})

    for key, value in updated_task_info.items():
        existing_task[key]=value

    data[task_id]=existing_task

    save_data(data)
    return JSONResponse(status_code=200, content={"message":"Task updated successfully"})

@app.delete("/delete/{task_id}")
def delete_task(task_id: str):
    data = load_data()
    if task_id not in data:
        raise HTTPException(404, detail="Task not found")
    del data[task_id]
    save_data(data)
    return JSONResponse(status_code=200, content={"message":"Task deleted successfully"})