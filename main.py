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

cursor = db.cursor()

# Что сегодня на обед?
@app.get('/get_lunch_list')
def get_lunch_list(chat_id):
    query = QUERIES['get_lunch_list'].format(chat_id = chat_id)
    cursor.execute(query)
    lunch = cursor.fetchall()
    return lunch

def update_user_lunch_id(lunch_id, chat_id):
    query = QUERIES['update_user_lunch_id'].format(lunch_id = lunch_id, chat_id = chat_id)
    cursor.execute(query)

# Проголосовать за обед
@app.post('/vote')
def update_lunch_votes_count(lunch_id, chat_id):
    update_user_lunch_id(lunch_id, chat_id)
    
    query = QUERIES['update_lunch_votes_count'].format(lunch_id = lunch_id, chat_id = chat_id)
    cursor.execute(query)

# Добавить вариант обеда
@app.post('/add_lunch')
def add_lunch(lunch: Lunch):
    query = QUERIES['add_lunch'].format(lunch_name = lunch.name, company_id = lunch.company_id)
    cursor.execute(query)

# Кто завтра в офис?
@app.get('/office')
def get_users(chat_id):
    query = QUERIES['get_users'].format(chat_id = chat_id)
    cursor.execute(query)
    users = cursor.fetchall()
    return users

# Я завтра в офис!
@app.post('/office')
def update_user_presence(user: User):
    query = QUERIES['update_user_presence'].format(present = user.present, chat_id = user.chat_id)
    cursor.execute(query)

@app.post('/add_company')
def add_company(company: Company):
    query = QUERIES['add_company'].format(company_name = company.name, company_code = company.code)
    cursor.execute(query)

@app.get('/get_companies')
def get_companies():
    query = QUERIES['get_companies']
    cursor.execute(query)
    companies = cursor.fetchall()
    return companies

def company_name_by_code(code):
    query = QUERIES['get_company_name_by_code'].format(code = code)
    cursor.execute(query)
    name = cursor.fetchall()
    return name

@app.post('/add_user')
def add_user(name, chat_id, company_code):
    query = QUERIES['add_user'].format(name = name, chat_id = chat_id, company_code = company_code)
    try:
        cursor.execute(query)
        db.commit()
    except:
        raise HTTPException(status_code = 404, detail = 'Company not found')
    return company_name_by_code(company_code)

def main():
    run(app, host="localhost", port=8001)

if __name__ == "__main__":
    main()
