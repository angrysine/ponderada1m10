from fastapi import APIRouter, Depends
import sqlite3
from models.task import Task, TaskWithoutContent
from routers.user import getUser
from typing_extensions import Annotated

router = APIRouter()

@router.post('/addTask')
async def addTask(task:Task,token:Annotated[dict, Depends(getUser)]):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    title = task.title
    content = task.content
    if not content:
        return {"status": "failed content is required"}
    username = token['user']
    cur.execute("SELECT * FROM tasks WHERE title = ? AND username = ?", (title, username))
    task = cur.fetchone()
    if task:
        return {"status": "failed task already exists"}
    cur.execute("INSERT INTO tasks (title, content, username) VALUES (?, ?, ?)", (title, content, username,))
    con.commit()
    return {"status": "success creating task with title: " + title}

@router.get('/getTasks')
async def getTasks( token:Annotated[dict, Depends(getUser)]):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    username = token['user']
    cur.execute("SELECT * FROM tasks WHERE username = ?", (username,))
    tasks = cur.fetchall()
    tasks = [{"title": task[0], "content": task[1]} for task in tasks]
    return {"tasks": tasks}

@router.delete('/deleteTask')
async def deleteTask(task: TaskWithoutContent, token:Annotated[dict, Depends(getUser)]):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    username = token['user']
    title = task.title
    cur.execute("SELECT * FROM tasks WHERE title = ? AND username = ?", (title, username,))
    task = cur.fetchone()
    if not task:
        return {"status": "failed task not found"}
    cur.execute("DELETE FROM tasks WHERE title = ? AND username =?", (title,username))
    con.commit()
    return {"status": "success deleting task with title: " + title}

@router.put('/updateTask')
async def updateTask(task: Task,token : Annotated[dict, Depends(getUser)]):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    username = token['user']
    title = task.title
    content = task.content
    cur.execute("SELECT * FROM tasks WHERE title = ? AND username = ?", (title, username))
    task = cur.fetchone()
    if not task:
        return {"status": "failed task not found"}
    cur.execute("UPDATE tasks SET content = ? WHERE title = ? and username = ?", (content, title,username))
    con.commit()
    return {"status": "success updating task with title: " + title}
