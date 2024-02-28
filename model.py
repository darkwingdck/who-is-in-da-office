from pydantic import BaseModel

class Company(BaseModel):
    id: int = 0
    name: str
    employees_count: int = 0
    code: str

class Lunch(BaseModel):
    id: int = 0
    name: str
    votes_count: int = 0
    company_id: int

class User(BaseModel):
    id: int = 0
    name: str
    chat_id: str
    lunch_id: int = 0
    company_id: int
    present: bool = False
