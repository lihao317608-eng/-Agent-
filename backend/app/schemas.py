from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CreateTaskReq(BaseModel):
    topic: str
    platform: str = Field(pattern="^(xiaohongshu|wechat)$")
    count: int = Field(default=5, ge=1, le=50)
    use_evaluator: bool = True

class TaskResp(BaseModel):
    id: int
    topic: str
    platform: str
    count: int
    status: str
    trend_output: Optional[str] = None
    generated_output: Optional[str] = None
    rewritten_output: Optional[str] = None
    evaluated_output: Optional[str] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True
