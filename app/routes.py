from fastapi import APIRouter, HTTPException
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app import crud

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskResponse])
def list_tasks():
    return crud.get_all_tasks()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = crud.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    return crud.create_task(task)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate):
    updated = crud.update_task(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):
    if not crud.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")