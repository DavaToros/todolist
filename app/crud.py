from app.database import get_db_connection
from app.schemas import TaskCreate, TaskUpdate

def get_all_tasks():
    with get_db_connection() as conn:
        tasks = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
        return [dict(task) for task in tasks]

def get_task_by_id(task_id: int):
    with get_db_connection() as conn:
        task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return dict(task) if task else None

def create_task(task: TaskCreate):
    with get_db_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (task.title, task.description)
        )
        conn.commit()
        new_id = cursor.lastrowid
        return get_task_by_id(new_id)

def update_task(task_id: int, task: TaskUpdate):
    with get_db_connection() as conn:
        existing = get_task_by_id(task_id)
        if not existing:
            return None

        updates = []
        params = []
        if task.title is not None:
            updates.append("title = ?")
            params.append(task.title)
        if task.description is not None:
            updates.append("description = ?")
            params.append(task.description)
        if task.completed is not None:
            updates.append("completed = ?")
            params.append(task.completed)

        if updates:
            params.append(task_id)
            conn.execute(
                f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?",
                params
            )
            conn.commit()
        return get_task_by_id(task_id)

def delete_task(task_id: int):
    with get_db_connection() as conn:
        existing = get_task_by_id(task_id)
        if not existing:
            return False
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return True