import sqlite3


class KBDatabase(object):
    def __init__(self):
        print('Initialize database controller...')

    def setup_database(self):
        conn = None

        try:
            conn = sqlite3.connect('knowledgebase.db')
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS kbase"
                      "(id INTEGER,"
                      "full_name VARCHAR,"
                      "trust_score REAL,"
                      "PRIMARY KEY(id))")

            print('Finished set-up for knowledge base!')

            c.close()
        except Exception as e:
            print(e)
