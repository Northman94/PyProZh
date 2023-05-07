
import sqlite3


def create_table():
    try:
        conn = sqlite3.connect("user_L4.db")
        cur = conn.cursor()

        # Check if table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        result = cur.fetchone()

        # Create table if it doesn't exist
        if not result:
            cur.execute('''CREATE TABLE users
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          nickname TEXT NOT NULL UNIQUE,
                          password TEXT NOT NULL,
                          house TEXT,
                          magic_item_level TEXT)''')
        conn.commit()

    finally:
        conn.close()


def get_user_info(nick):
    try:
        conn = sqlite3.connect("user_L4.db")
        cur = conn.cursor()

        sql = """
            SELECT nickname FROM users;  
        """

        res = cur.execute(sql)
        print('1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        db_content = res.fetchall()
        print(db_content)
        print('2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(nick)

        for usr in db_content:
            print(f"Check: {usr}")
            if usr[0] == nick:
                return True
            else:
                return False

    finally:
        conn.close()




def put_user_info():

    sql = """
    INSERT INTO users VALUES()
    """

    pass