from pydantic import BaseModel

class Company(BaseModel):
    id: int
    name: str
    employees_count: int = 0
    code: str

class Lunch(BaseModel):
    id: int
    name: str
    votes_count: int = 0
    company_id: int

class User(BaseModel):
    id: int
    name: str
    chat_id: str
    lunch_id: int
    company_id: int
    present_tomorrow: bool
