from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="Simple CRUD API for managing tasks",
    version="1.0"
)

tasks = [
    {"id": 1, "title": "Study FastAPI", "done": False},
    {"id": 2, "title": "Do DSA", "done": True},
    {"id": 3, "title": "Push to GitHub", "done": False}
]


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool


@app.get("/", summary="API Information")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", summary="Health Check")
def health():
    return {"status": "ok"}


@app.get("/tasks", summary="Get all tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", summary="Get task by ID")
def get_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.post("/tasks", status_code=201, summary="Create a task")
def create_task(task: TaskCreate):

    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )

    new_task = {
        "id": max([t["id"] for t in tasks], default=0) + 1,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, updated: TaskUpdate):

    if not updated.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated.title
            task["done"] = updated.done
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )