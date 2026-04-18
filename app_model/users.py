def add_user(conn, name, password_hash):
    cur = conn.cursor()
    sql = '''INSERT OR REPLACE INTO users (username, password_hash) VALUES (?, ?)'''
    cur.execute(sql, (name, password_hash))
    conn.commit()

def migrate_users(conn):
    with open('DATA/users.txt', 'r') as f:
        users = f.readlines()

    for user in users:
        name, password_hash = user.strip().split(',')
        add_user(conn, name, password_hash)

def get_all_users(conn):
    cur = conn.cursor()
    sql = '''SELECT * FROM users'''
    cur.execute(sql)
    return cur.fetchall()

def get_user(conn, name):
    cur = conn.cursor()
    sql = '''SELECT * FROM users WHERE username = ?'''
    cur.execute(sql, (name,))
    return cur.fetchone()

def update_user(conn, old_name, new_name):
    cur = conn.cursor()
    sql = 'UPDATE users SET username = ? WHERE username = ?'
    cur.execute(sql, (new_name, old_name))
    conn.commit()

def delete_user(conn, user_name):
    cur = conn.cursor()
    sql = 'DELETE FROM users WHERE username = ?'
    cur.execute(sql, (user_name,))
    conn.commit()