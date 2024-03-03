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

def get_company_name_by_id(id):
    query = QUERIES['get_company_name_by_id'].format(id=id)
    cursor.execute(query)
    name = cursor.fetchone()[0]
    return name

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
        return get_company_name_by_id(user.company_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/users')
def get_users(user_id):
    query = QUERIES['get_users'].format(user_id=user_id)
    cursor.execute(query)
    users = cursor.fetchall()
    return users

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
        # updating user lunch
        pass

@app.get('/users/{user_id}')
def get_user(user_id: str):
    try:
        query = QUERIES['get_user'].format(id=user_id)
        cursor.execute(query)
        user = cursor.fetchone()
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
######################
@app.get('/lunch')
def get_lunch_list(chat_id):
    query = QUERIES['get_lunch_list'].format(chat_id=chat_id)
    cursor.execute(query)
    lunch = cursor.fetchall()
    return lunch

def update_user_lunch_id(lunch_id, chat_id):
    query = QUERIES['update_user_lunch_id'].format(lunch_id=lunch_id, chat_id=chat_id)
    cursor.execute(query)

# Проголосовать за обед
@app.post('/vote')
def update_lunch_votes_count(lunch_id, chat_id):
    update_user_lunch_id(lunch_id, chat_id)

    query = QUERIES['update_lunch_votes_count'].format(lunch_id=lunch_id, chat_id=chat_id)
    cursor.execute(query)

# Добавить вариант обеда
@app.post('/add_lunch')
def add_lunch(lunch: Lunch):
    query = QUERIES['add_lunch'].format(lunch_name=lunch.name, company_id=lunch.company_id)
    cursor.execute(query)


@app.post('/add_company')
def add_company(company: Company):
    query = QUERIES['add_company'].format(company_name=company.name, company_code=company.code)
    cursor.execute(query)

@app.get('/get_companies')
def get_companies():
    query = QUERIES['get_companies']
    cursor.execute(query)
    companies = cursor.fetchall()
    return companies

def main():
    run(app, host="localhost", port=8001)

if __name__ == "__main__":
    main()
