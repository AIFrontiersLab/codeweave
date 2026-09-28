from typing import Dict, List
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI(title="Diff Builder MVP")

class TaskRequest(BaseModel):
    query: str
    files: Dict[str, str]

class DiffEntry(BaseModel):
    file: str
    action: str
    old: str = ""
    new: str = ""

class TaskResponse(BaseModel):
    task_id: str
    status: str
    diffs: List[DiffEntry]

def compute_diffs(query: str, files: Dict[str, str]) -> List[DiffEntry]:
    diffs = []
    query_lower = query.lower()
    for filename, content in files.items():
        if "add" in query_lower:
            diffs.append(DiffEntry(
                file=filename,
                action="add",
                new="new_code_here"
            ))
        elif "remove" in query_lower:
            diffs.append(DiffEntry(
                file=filename,
                action="remove",
                old=content
            ))
        elif "replace" in query_lower or "change" in query_lower:
            parts = query.split()
            if len(parts) >= 4:
                old_val = parts[2]
                new_val = parts[4] if len(parts) > 4 else "updated_value"
                diffs.append(DiffEntry(
                    file=filename,
                    action="replace",
                    old=old_val,
                    new=new_val
                ))
            else:
                diffs.append(DiffEntry(
                    file=filename,
                    action="replace",
                    old="unknown",
                    new="updated_value"
                ))
        else:
            diffs.append(DiffEntry(
                file=filename,
                action="noop",
                old=content,
                new=content
            ))
    return diffs

@app.post("/task", response_model=TaskResponse)
async def process_task(req: TaskRequest):
    task_id = f"task-{len(req.files)}"
    diffs = compute_diffs(req.query, req.files)
    return TaskResponse(
        task_id=task_id,
        status="completed",
        diffs=diffs
    )

def demo():
    result = process_task(TaskRequest(
        query="change missing to present",
        files={"main.py": "print('hello')"}
    ))
    print(f"Task ID: {result.task_id}")
    print(f"Status: {result.status}")
    for d in result.diffs:
        print(f"  {d.file}: {d.action} ({d.old} -> {d.new})")
