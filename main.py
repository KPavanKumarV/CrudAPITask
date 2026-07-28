from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="Task API", version="1.0")

# In-memory "database"
tasks = [
    {"id": 1, "title": "Setup repository", "done": True},
    {"id": 2, "title": "Build CRUD endpoints", "done": False},
    {"id": 3, "title": "Deploy to production", "done": False},
]

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks

# Get a single task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    # Raise a clear 404 error if not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Task {task_id} not found"
    )