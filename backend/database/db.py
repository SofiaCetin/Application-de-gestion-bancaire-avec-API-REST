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
            balance NUMERIC(12, 2)
            )     
        """)

        conn.commit()
        cur.close()
        conn.close()
    
    def register(self, id : str, first : str, last: str, password : str, balance : float):
    
        conn = self.connect()
        cur = conn.cursor()
    
        cur.execute("""
            INSERT INTO accounts (id, first, last, pass, balance)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            RETURNING id
            """, (id, first, last, password, balance))
        res = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if res:
            return res[0]
        else:
            return None
        
    def get_first(self, id : str):
        
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT first
            FROM accounts
            WHERE id = %s
            """, (id,))
        
        res = cur.fetchone()
        cur.close()
        conn.close()
        if res:
            return res[0]
        else:
            return None
    
    def get_last(self, id : str):
        
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT last
            FROM accounts
            WHERE id = %s
            """, (id,))
        
        res = cur.fetchone()
        cur.close()
        conn.close()
        if res:
            return res[0]
        else:
            return None
    
    def get_user(self, id : str):
        
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT *
            FROM accounts
            WHERE id = %s
            """, (id,))
        
        res = cur.fetchone()
        cur.close()
        conn.close()
        if res:
            return res[0]
        else:
            return None
        
    
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
        if res:
            return res[0]
        else:
            return None
    
    def get_balance(self, id : str):
    
        conn = self.connect()
        cur = conn.cursor()
    
        cur.execute("""
            SELECT balance
            FROM accounts
            WHERE id = %s
            """, (id ,))
    
        res = cur.fetchone()
        cur.close()
        conn.close()
        if res:
            return res[0]
        else:
            return None
    
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
    
    def set_balance(self, id : str, balance : float):
        
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE accounts
            SET balance = %s
            WHERE id = %s
            """, (balance, id))
        
        conn.commit()
        cur.close()
        conn.close()
    
    def transfer(self, transmitter_id : str, receiver_id : str, amount : float):
        
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE accounts
            SET balance = balance - %s
            WHERE id = %s
            """, (amount, transmitter_id))
        
        cur.execute("""
            UPDATE accounts
            SET balance = balance + %s
            WHERE id = %s
            """, (amount, receiver_id))
        
        conn.commit()
        cur.close()
        conn.close()