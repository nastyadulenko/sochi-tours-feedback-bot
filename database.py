import sqlite3
from datetime import datetime

DB_NAME = 'reviews.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tour_name TEXT,
                rating INTEGER,
                feedback TEXT,
                username TEXT,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("База данных готова")

def save_review(tour_name, rating, feedback, username, user_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            'INSERT INTO reviews (tour_name, rating, feedback, username, user_id) VALUES (?, ?, ?, ?, ?)',
            (tour_name, rating, feedback, username, user_id)
        )

def get_stats():
    with sqlite3.connect(DB_NAME) as conn:
        avg = conn.execute('SELECT AVG(rating) FROM reviews').fetchone()[0]
        total = conn.execute('SELECT COUNT(*) FROM reviews').fetchone()[0]
        
        counts = {}
        for i in range(1, 6):
            cnt = conn.execute('SELECT COUNT(*) FROM reviews WHERE rating = ?', (i,)).fetchone()[0]
            counts[i] = cnt
            
        return {
            'avg': round(avg, 2) if avg else 0,
            'total': total,
            'counts': counts
        }

def get_reviews(limit=10):
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute('SELECT * FROM reviews ORDER BY created_at DESC LIMIT ?', (limit,))
        return cursor.fetchall()