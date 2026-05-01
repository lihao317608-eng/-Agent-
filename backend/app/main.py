from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import User, ContentTask
from .schemas import UserCreate, Token, CreateTaskReq, TaskResp
from .auth import hash_password, verify_password, create_access_token, get_current_user
from .tasks import run_content_pipeline

Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI Content Production API")

@app.post('/auth/register', response_model=Token)
def register(req: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.username == req.username).first()
    if exists:
        raise HTTPException(400, 'username exists')
    user = User(username=req.username, hashed_password=hash_password(req.password))
    db.add(user)
    db.commit()
    return Token(access_token=create_access_token(req.username))

@app.post('/auth/login', response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, 'bad credentials')
    return Token(access_token=create_access_token(user.username))

@app.post('/tasks', response_model=TaskResp)
def create_task(req: CreateTaskReq, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = ContentTask(owner_id=user.id, topic=req.topic, platform=req.platform, count=req.count)
    db.add(task)
    db.commit()
    db.refresh(task)
    run_content_pipeline.delay(task.id, req.use_evaluator)
    return task

@app.get('/tasks/{task_id}', response_model=TaskResp)
def get_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = db.query(ContentTask).filter(ContentTask.id == task_id, ContentTask.owner_id == user.id).first()
    if not task:
        raise HTTPException(404, 'not found')
    return task
