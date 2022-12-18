import sqlite3
from sqlite3 import Error


# connect to the sqlite database
def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


# create a function to insert names manually into the database
def create_name(conn, name):
    """
    Create a new name
    :param conn:
    :param name:
    :return:
    """

    sql = ''' INSERT INTO kbase(full_name, trust_score)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, name)
    conn.commit()

    return cur.lastrowid


def main():
    db = 'knowledgebase.db'

    conn = create_connection(db)
    with conn:
        name1 = ('Tim Turner', 4.5)
        name2 = ('Harry Hunter', 6.7)

        create_name(conn, name1)
        create_name(conn, name2)


if __name__ == '__main__':
    main()
