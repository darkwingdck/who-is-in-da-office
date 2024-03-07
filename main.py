from fastapi import FastAPI, HTTPException
from mysql.connector import connect
from uvicorn import run
from queries import QUERIES
from model import Company, Lunch, User

app = FastAPI()

db = connect(
    host = "localhost",
    user = "root",
    password = "mint",
    database = "office_database"
)

cursor = db.cursor(buffered=True)

# users
@app.post('/users')
def add_user(user: User):
    query = QUERIES['add_user'].format(
        id = user.id,
        name = user.name,
        company_id = user.company_id
    )
    try:
        cursor.execute(query)
        db.commit()
        return get_company(user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/users')
def get_users(user_id):
    query = QUERIES['get_users'].format(user_id=user_id)
    cursor.execute(query)
    users_rows = cursor.fetchall()
    res = {}
    for user in users_rows:
        id, name = user
        res[id] = name
    return res

@app.put('/users')
def update_user(user: User):
    if not user.presence is None:
        try:
            query = QUERIES['update_user_presence'].format(id=user.id, presence=user.presence)
            cursor.execute(query)
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    elif not user.lunch_id is None:
        try:
            query = QUERIES['update_user_lunch_id'].format(id=user.id, lunch_id=user.lunch_id)
            cursor.execute(query)
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get('/users/{user_id}')
def get_user(user_id: str):
    try:
        query = QUERIES['get_user'].format(id=user_id)
        cursor.execute(query)
        user = cursor.fetchone()
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# lunch
@app.get('/lunches')
def get_lunches(user_id):
    query = QUERIES['get_lunches'].format(user_id=user_id)
    cursor.execute(query)
    lunches = cursor.fetchall()
    return lunches

@app.post('/lunches')
def add_lunch(lunch: Lunch):
    query = QUERIES['add_lunch'].format(name=lunch.name, company_id=lunch.company_id)
    cursor.execute(query)
    db.commit()

@app.put('/lunches')
def update_lunch(lunch: Lunch, change_direction='1'):
    if lunch.votes_count is None: return
    try:
        if change_direction == '1':
            query = QUERIES['increase_lunch_votes_count'].format(id=lunch.id)
        else:
            query = QUERIES['decrease_lunch_votes_count'].format(id=lunch.id)
        cursor.execute(query)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_user_lunch_id(lunch_id, chat_id):
    query = QUERIES['update_user_lunch_id'].format(lunch_id=lunch_id, chat_id=chat_id)
    cursor.execute(query)

# company
@app.post('/company')
def add_company(company: Company):
    query = QUERIES['add_company'].format(
        id = company.id,
        name = company.name,
    )
    try:
        cursor.execute(query)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/company')
def get_companies():
    query = QUERIES['get_companies']
    try:
        cursor.execute(query)
        companies_rows = cursor.fetchall()
        res = {}
        for company in companies_rows:
            id, name, employees_count = company
            res[id] = {
                'name': name,
                'employees_count': employees_count
            }
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/company/{user_id}')
def get_company(user_id: str) -> dict:
    try:
        query = QUERIES['get_company'].format(user_id=user_id)
        cursor.execute(query)
        company_row = cursor.fetchone()
        if company_row:
            id, name, employees_count = company_row
            return {
                'id': id,
                'name': name,
                'employees_count': employees_count
            }
        return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def main():
    run(app, host="localhost", port=8001)

if __name__ == "__main__":
    main()
