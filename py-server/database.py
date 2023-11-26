import sqlite3
from contextlib import contextmanager

DATABASE_PATH = 'game.db'

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def create_table():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                position_x INTEGER,
                position_y INTEGER,
                health INTEGER,
                action_points REAL,
                last_update_time REAL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        conn.commit()

def save_player(player_dict):
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO players(player_id, user_id, name, position_x, position_y, health, action_points, last_update_time)
            VALUES(:player_id, :user_id, :name, :position_x, :position_y, :health, :action_points, :last_update_time)
            ON CONFLICT(player_id) DO UPDATE SET
                user_id = excluded.user_id,
                name = excluded.name,
                position_x = excluded.position_x,
                position_y = excluded.position_y,
                health = excluded.health,
                action_points = excluded.action_points,
                last_update_time = excluded.last_update_time
        ''', player_dict)
        conn.commit()

def get_player(player_id):
    with get_db_connection() as conn:
        cursor = conn.execute('SELECT * FROM players WHERE player_id = ?', (player_id,))
        row = cursor.fetchone()
        if row:
            keys = ['player_id', 'user_id', 'name', 'position_x', 'position_y', 'health', 'action_points', 'last_update_time']
            return dict(zip(keys, row))
    return None


