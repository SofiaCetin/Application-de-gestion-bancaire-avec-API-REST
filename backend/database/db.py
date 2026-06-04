import psycopg2, os

class Database:
    
    
    def __init__(self, database_url):
        
        self.database_link = database_url
    
    

    def connect(self):
        return psycopg2.connect(self.database_link)

    def init(self):

        conn = self.connect()

        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS accounts(
            id TEXT PRIMARY KEY,
            first TEXT,
            last TEXT,
            pass TEXT,
            token TEXT,
            wallet NUMERIC(12, 2)
            )     
        """)

        conn.commit()
        cur.close()
        conn.close()
    
    def register(self, id : str, first : str, last: str, password : str, wallet : float):
    
        conn = self.connect()
        cur = conn.cursor()
    
        cur.execute("""
            INSERT INTO accounts (id, first, last, pass, wallet)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            RETURNING id
            """, (id, first, last, password, wallet))
        res = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
    
        return res
    
    def get_pass(self, id : str):
    
        conn = self.connect()
        cur = conn.cursor()
    
        cur.execute("""
            SELECT pass
            FROM accounts
            WHERE id = %s
            """, (id ,))
    
        res = cur.fetchone()
        cur.close()
        conn.close()
        return res
    
    def set_token(self, id : str, token : str):
    
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE accounts
            SET token = %s
            WHERE id = %s
            """, (token, id))
        
        conn.commit()
        cur.close()
        conn.close()
    
    def set_pass(self, id : str, password : str):
        
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE accounts
            SET pass = %s
            WHERE id = %s
            """, (password, id))
        
        conn.commit()
        cur.close()
        conn.close()