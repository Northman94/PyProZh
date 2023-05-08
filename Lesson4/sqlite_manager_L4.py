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


def check_user(nick, password):
    try:
        conn = sqlite3.connect("user_L4.db")
        cur = conn.cursor()

        sql = """
            SELECT nickname, password, house, magic_item_level FROM users;  
        """

        res = cur.execute(sql)
        db_content = res.fetchall()
        # Return all DB lines (List of Tuples):
        print(f"1db_content: {db_content}")

        # usr = one Tuple at a Time
        # usr[0] / elm in usr = first cell of every Tuple

        for usr in db_content:
            print(f"Show next tuple: {usr}")
            if usr[0] == nick and usr[1] == password:
                return True
        return False

    finally:
        conn.close()


def put_user_info(u_nickname, u_password, h_house, item_level):
    try:
        conn = sqlite3.connect("user_L4.db")
        cur = conn.cursor()

        sql = f"""
        INSERT INTO users (nickname, password, house, magic_item_level)
        VALUES(?, ?, ?, ?)
        """

        cur.execute(sql, (u_nickname, u_password, h_house, item_level))
        conn.commit()

    finally:
        conn.close()


def get_all_info(u_nickname, u_password):
    try:
        conn = sqlite3.connect("user_L4.db")
        cur = conn.cursor()

        sql = """
            SELECT nickname, password, house, magic_item_level FROM users;  
        """

        res = cur.execute(sql)
        all_user_info = res.fetchall()
        # Return all DB lines (List of Tuples):
        print(f"db_content: {all_user_info}")

        for tuple_line in all_user_info:
            print(f"Tuple line: {tuple_line}")
            if u_nickname and u_password in tuple_line:
                return tuple_line
        raise Exception("DB Error")

    finally:
        conn.close()