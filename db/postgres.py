import psycopg2


class Database():
    def __init__(self):
        self.params = {
            "host": "localhost",
            "database": "postgres",
            "user": "postgres",
            "password": "123456"
        }
        self.conn = None
        self.cursor = None
        self.open()

    def open(self):
        self.conn = psycopg2.connect(**self.params)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def execute(self, sql: str, data: tuple, many: bool = False):
        rows = None
        self.cursor.execute(sql, data)
        if many:
            rows = self.cursor.fetchall()
        else:
            rows = self.cursor.fetchone()
        return rows

    def getCounter(self):
        query = "SELECT counter from cronconfig;"
        self.cursor.execute(query)
        rows = self.cursor.fetchone()
        return rows[0]
    
    def updateCounter(self, data: tuple):
        sql = "UPDATE cronconfig SET counter = %s RETURNING counter;"
        self.cursor.execute(sql, data)
        rows = self.cursor.fetchone()[0]
        return rows
