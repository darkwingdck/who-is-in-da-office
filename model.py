from typing import Optional
from pydantic import BaseModel, Field

class Company(BaseModel):
    id: str = ''
    name: str = ''
    employees_count: int = 0

class Lunch(BaseModel):
    id: int = 0
    name: str = ''
    votes_count: int = 1
    company_id: str

class User(BaseModel):
    id: str = Field(..., description='The user ID is required')
    name: Optional[str] = None
    lunch_id: Optional[int] = None
    company_id: Optional[str] = None
    presence: Optional[bool] = None
