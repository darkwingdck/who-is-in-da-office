import logging

from mysql.connector import connect
from queries import QUERIES
from server.config import DB_DATABASE, DB_HOST, DB_PASSWORD, DB_USER

db = connect(
    host = DB_HOST,
    user = DB_USER,
    password = DB_PASSWORD,
    database = DB_DATABASE
)

cursor = db.cursor(buffered=True)

logging.basicConfig(
    filename='logs/reset_db.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def reset_db():
    user_lunch_query = QUERIES['reset_user_lunch_id'].format()
    user_presence_query = QUERIES['reset_user_presence'].format()
    lunch_query = QUERIES['reset_lunch'].format()
    try:
        cursor.execute(user_lunch_query)
        cursor.execute(user_presence_query)
        cursor.execute(lunch_query)
        db.commit()
    except Exception as e:
        logging.error(str(e))

if __name__ == "__main__":
    reset_db()
