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

        for usr in db_content:
            print(f"Part: {usr}")
            if usr[0] == nick and usr[1] == password:
                print(f"usr[0]: {usr[0]}")
                print(f"nick: {nick}")
                print(f"usr[1]: {usr[1]}")
                print(f"password: {password}")
                return True
            else:
                return False

            # for usr in db_content:
            #     print(f"usr: {usr}")
            #     print(f"usr[0]: {usr[0]}")
            #     print(f"nick: {nick}")
            #     if usr[0] == nick:
            #         return usr



    finally:
        conn.close()


def put_user_info(n, p, h, m):
    try:
        conn = sqlite3.connect("user_L4.db")
        cur = conn.cursor()

        print(f"Passed Nickname: {n}") #+
        print(f"Passed Password: {p}") #+
        print(f"Passed House: {h}") #+
        print(f"Passed m_item: {m}") #+

        sql = f"""
        INSERT INTO users (nickname, password, house, magic_item_level)
        VALUES(?, ?, ?, ?)
        """

        cur.execute(sql, (n, p, h, m))
        conn.commit()

    finally:
        conn.close()
