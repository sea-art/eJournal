import sqlite3

database = 'VLE.db'

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


if __name__=='__main__':
    tables = ["user", "course", "assignment", "journal"]
    conn = create_connection(database)
    for table in tables:
        print(table)
        cur = conn.cursor()
        cur.execute("SELECT * FROM VLE_{}".format(table))
        for row in cur.fetchall():
            print(row)
        print()
    conn.close()
