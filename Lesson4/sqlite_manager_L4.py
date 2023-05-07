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


def get_user_info(nick, password, get_all_info):
    try:
        conn = sqlite3.connect("user_L4.db")
        cur = conn.cursor()

        sql = """
            SELECT nickname, password, house, magic_item_level FROM users;  
        """

        res = cur.execute(sql)
        db_content = res.fetchall()

        if get_all_info:
            for usr in db_content:
                print(usr)
                print(f"5!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(usr[0])
                print(nick)
                #if usr[0] == nick:
                return usr

        else:
            for usr in db_content:
                print(f"Part: {usr}")
                if usr[0] == nick and usr[1] == password:
                    return True
                else:
                    return False

    finally:
        conn.close()


def put_user_info(nickname, password, house, magic_item):
    try:
        conn = sqlite3.connect("user_L4.db")
        cur = conn.cursor()

        sql = """
        INSERT INTO users (nickname, password, house, magic_item_level)
        VALUES('{}', '{}', '{}', {});
        """.format(nickname, password, house, magic_item)

        res = cur.execute(sql)

        db_content = res.fetchall()
        print(db_content)

    finally:
        conn.close()
