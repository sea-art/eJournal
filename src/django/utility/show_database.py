import sqlite3


def create_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return None


if __name__ == '__main__':
    database = 'VLE.db'
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

