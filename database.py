import sqlite3
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY").encode()  # Load the encryption key from .env
cipher = Fernet(ENCRYPTION_KEY)

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS servers (
            user_id TEXT,
            name TEXT,
            ip TEXT,
            ssh_user TEXT,
            ssh_password TEXT,
            port INTEGER DEFAULT 22, -- Add port field with default 22
            PRIMARY KEY (user_id, name)
        )
        """
        self.conn.execute(query)
        self.conn.commit()
    
    def list_servers(self, user_id):
        query = "SELECT name, ip FROM servers WHERE user_id = ?"
        return self.conn.execute(query, (user_id,)).fetchall()

    def encrypt_password(self, plaintext_password):
        return cipher.encrypt(plaintext_password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        return cipher.decrypt(encrypted_password.encode()).decode()

    def add_server(self, user_id, name, ip, ssh_user, ssh_password, port=22):
        encrypted_password = self.encrypt_password(ssh_password)
        try:
            query = "INSERT INTO servers (user_id, name, ip, ssh_user, ssh_password, port) VALUES (?, ?, ?, ?, ?, ?)"
            self.conn.execute(query, (user_id, name, ip, ssh_user, encrypted_password, port))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_server(self, user_id, name):
        query = "SELECT name, ip, ssh_user, ssh_password, port FROM servers WHERE user_id = ? AND name = ?"
        result = self.conn.execute(query, (user_id, name)).fetchone()
        if result:
            name, ip, ssh_user, encrypted_password, port = result
            decrypted_password = self.decrypt_password(encrypted_password)
            return (name, ip, ssh_user, decrypted_password, port)
        return None
    
    def delete_server(self, user_id, name):
        query = "DELETE FROM servers WHERE user_id = ? AND name = ?"
        self.conn.execute(query, (user_id, name))
        self.conn.commit()
        return self.conn.total_changes > 0
