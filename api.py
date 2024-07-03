import sqlite3
import datetime

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_tables()

    def create_connection(self):
        conn = sqlite3.connect(self.db_file)
        return conn, conn.cursor()

    def create_tables(self):
        conn, cursor = self.create_connection()
        with conn:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    username TEXT,
                    phone_number TEXT,
                    date_created TEXT
                )
            ''')

    def userExists(self, user_id):
        conn, cursor = self.create_connection()
        cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def registerUser(self, user_id, from_user):
        if not self.userExists(user_id):
            conn, cursor = self.create_connection()
            with conn:
                cursor.execute('''
                    INSERT INTO users (user_id, first_name, last_name, username, date_created)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, from_user.first_name, from_user.last_name, from_user.username, str(datetime.datetime.now())))
            conn.close()
            return True
        return False


    def getUsers(self):
        conn, cursor = self.create_connection()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        return users

    def getUser(self, user_id):
        conn, cursor = self.create_connection()
        cursor.execute(f"SELECT * FROM users WHERE user_id={user_id}")
        users = cursor.fetchone()
        conn.close()
        return users

    def setPhoneNumber(self, user_id, phone_number):
        if not self.userExists(user_id):
            return False
        conn, cursor = self.create_connection()
        cursor.execute(f"UPDATE users SET phone_number = {phone_number} WHERE user_id={user_id}")
        conn.commit()
        conn.close()