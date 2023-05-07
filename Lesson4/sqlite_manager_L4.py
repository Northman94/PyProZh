
import sqlite3


def create_table():
    try:
        # Will crate table if not exists
        conn = sqlite3.connect("user_L4.db")
        cur = conn.cursor()

        sql = """
            CREATE TABLE users(nickname text UNIQUE, password text, house text, magic_item_level text)
        """
        cur.execute(sql)
        print(cur.fetchall())

    finally:
        conn.close()


def get_user_info(a,b):
    try:
        conn = sqlite3.connect("user_L4.db")
        cur = conn.cursor()

        sql = """
            SELECT * FROM users;
        """
        cur.execute(sql)
        print(cur.fetchall())

    finally:
        conn.close()




def put_user_info():
    pass