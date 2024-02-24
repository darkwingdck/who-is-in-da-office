from fastapi import FastAPI
from mysql.connector import connect
from uvicorn import run
from queries import QUERIES

app = FastAPI()

db = connect(
    host = "localhost",
    user = "root",
    password = "mint",
    database = "office_database"
)

cursor = db.cursor()

@app.get('/')
def root():
    return { 'Hello': 'World!' }

# Что сегодня на обед?
@app.get('/get_lunch_list')
def get_lunch_list(company_id):
    query = QUERIES['get_lunch'].format(company_id)
    cursor.execute(query)
    lunch = cursor.fetchall()
    return lunch

def update_user_lunch_id(lunch_id, user_id, company_id):
    query = QUERIES['update_user_lunch_id'].format(lunch_id, user_id, company_id)
    cursor.execute(query)

# Проголосовать за обед
@app.post('/vote')
def update_lunch_votes_count(user_id, company_id, lunch_id):
    update_user_lunch_id(lunch_id, user_id, company_id)
    
    query = QUERIES['update_lunch_votes_count'].format(lunch_id, company_id)
    cursor.execute(query)

# Добавить вариант обеда
@app.post('/add_lunch')
def add_lunch(lunch_name, company_id):
    query = QUERIES['add_lunch'].format(lunch_name, company_id)
    cursor.execute(query)

# Кто завтра в офис?
@app.get('/office')
def get_users(company_id):
    query = QUERIES['get_users'].format(company_id)
    cursor.execute(query)
    users = cursor.fetchall()
    return users

# Я завтра в офис!
@app.post('/office')
def update_user_presence(user_id, present_tomorrow):
    query = QUERIES['update_user_presence'].format(present_tomorrow, user_id)
    cursor.execute(query)

@app.post('/add_company')
def add_company(name, code):
    query = QUERIES['add_company'].format(name, code)
    cursor.execute(query)

@app.post('/add_user')
def add_user(name, chat_id, company_id):
    query = QUERIES['add_user'].format(name, chat_id, company_id)
    cursor.execute(query)

def main():
    run(app, host="localhost", port=8000)

if __name__ == "__main__":
    main()

