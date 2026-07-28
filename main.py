from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Task API", version="1.0")

tasks = [
    {"id": 1, "title": "Setup repository", "done": True},
    {"id": 2, "title": "Build CRUD endpoints", "done": False},
    {"id": 3, "title": "Deploy to production", "done": False},
]

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)

# Schema mapping updates
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    done: Optional[bool] = None

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_input: TaskCreate):
    if not task_input.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    new_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {"id": new_id, "title": task_input.title, "done": False}
    tasks.append(new_task)
    return new_task

# Update task completely/partially
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_input: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if task_input.title is not None:
                if not task_input.title.strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = task_input.title
            if task_input.done is not None:
                task["done"] = task_input.done
            return task
            
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

# Delete task (Returns status 204 No Content)
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
            
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")