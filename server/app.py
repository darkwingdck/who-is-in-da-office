import logging

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

logging.basicConfig(
    filename='../logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
        logging.error(str(e))
        raise HTTPException(status_code=500)

@app.get('/users')
def get_users(user_id):
    try:
        query = QUERIES['get_users'].format(user_id=user_id)
        cursor.execute(query)
        users_rows = cursor.fetchall()
        res = {}
        for user in users_rows:
            id, name = user
            res[id] = name
        return res
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500)

@app.put('/users')
def update_user(user: User):
    if not user.presence is None:
        try:
            query = QUERIES['update_user_presence'].format(id=user.id, presence=user.presence)
            cursor.execute(query)
            db.commit()
        except Exception as e:
            logging.error(str(e))
            raise HTTPException(status_code=500)
    elif not user.lunch_id is None:
        try:
            query = QUERIES['update_user_lunch_id'].format(id=user.id, lunch_id=user.lunch_id)
            cursor.execute(query)
            db.commit()
        except Exception as e:
            logging.error(str(e))
            raise HTTPException(status_code=500)

@app.get('/users/{user_id}')
def get_user(user_id: str):
    try:
        query = QUERIES['get_user'].format(id=user_id)
        cursor.execute(query)
        user_row = cursor.fetchall()[0]

        if not user_row: return {}

        return {
            'id': user_row[0],
            'name': user_row[1],
            'presence': user_row[2],
            'lunch_id': user_row[3],
            'company_id': user_row[4]
        }
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500)

# lunches
@app.get('/lunches')
def get_lunches(user_id):
    try:
        query = QUERIES['get_lunches'].format(user_id=user_id)
        cursor.execute(query)
        lunches = cursor.fetchall()
        return lunches
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500)

@app.post('/lunches')
def add_lunch(lunch: Lunch):
    try:
        query = QUERIES['add_lunch'].format(name=lunch.name, company_id=lunch.company_id)
        cursor.execute(query)
        db.commit()

        query = QUERIES['get_last_lunch']
        cursor.execute(query)
        lunch_id = cursor.fetchone()[0]
        return lunch_id
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500)

@app.put('/lunches')
def update_lunch(lunch: Lunch, change_direction='1'):
    try:
        if change_direction == '1':
            query = QUERIES['increase_lunch_votes_count'].format(id=lunch.id)
        else:
            query = QUERIES['decrease_lunch_votes_count'].format(id=lunch.id)
        cursor.execute(query)
        db.commit()
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500)

# company
@app.post('/companies')
def add_company(company: Company):
    try:
        query = QUERIES['add_company'].format(id=company.id, name=company.name)
        cursor.execute(query)
        db.commit()
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500)

@app.get('/companies')
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
        logging.error(str(e))
        raise HTTPException(status_code=500)

@app.get('/companies/{user_id}')
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
        logging.error(str(e))
        raise HTTPException(status_code=500)

def main():
    run(app, host="localhost", port=8001)

if __name__ == "__main__":
    main()
