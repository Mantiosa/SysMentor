import sqlite3

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
            PRIMARY KEY (user_id, name)
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_server(self, user_id, name, ip, ssh_user, ssh_password):
        try:
            query = "INSERT INTO servers (user_id, name, ip, ssh_user, ssh_password) VALUES (?, ?, ?, ?, ?)"
            self.conn.execute(query, (user_id, name, ip, ssh_user, ssh_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def list_servers(self, user_id):
        query = "SELECT name, ip FROM servers WHERE user_id = ?"
        return self.conn.execute(query, (user_id,)).fetchall()

    def delete_server(self, user_id, name):
        query = "DELETE FROM servers WHERE user_id = ? AND name = ?"
        self.conn.execute(query, (user_id, name))
        self.conn.commit()
        return self.conn.total_changes > 0

    def get_server(self, user_id, name):
        query = "SELECT * FROM servers WHERE user_id = ? AND name = ?"
        return self.conn.execute(query, (user_id, name)).fetchone()
