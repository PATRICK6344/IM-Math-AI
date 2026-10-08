import sqlite3

class KnowledgeBase:
    def __init__(self, db_path="im_pro_max.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.init_db()
        self.bootstrap_seed()

    def init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                concept TEXT,
                content TEXT,
                source TEXT,
                confidence REAL DEFAULT 0.5
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS theories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT,
                ai_message TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def bootstrap_seed(self):
        seed = [
            ("calculus", "derivative", "The derivative measures instantaneous change.", "seed", 0.95),
            ("calculus", "integral", "The integral accumulates quantity over an interval.", "seed", 0.95),
            ("algebra", "polynomial", "A polynomial is built from variables and coefficients.", "seed", 0.95),
            ("geometry", "symmetry", "Symmetry means invariance under transformation.", "seed", 0.95),
            ("topology", "continuity", "Continuity means nearby points remain nearby.", "seed", 0.95),
            ("number_theory", "prime", "A prime has exactly two positive divisors.", "seed", 0.95),
        ]
        for topic, concept, content, source, confidence in seed:
            existing = self.conn.execute(
                "SELECT 1 FROM facts WHERE topic=? AND concept=? AND content=? LIMIT 1",
                (topic, concept, content)
            ).fetchone()
            if existing is None:
                self.conn.execute(
                    "INSERT INTO facts(topic, concept, content, source, confidence) VALUES (?, ?, ?, ?, ?)",
                    (topic, concept, content, source, confidence)
                )
        self.conn.commit()

    def store_fact(self, topic, concept, content, source, confidence):
        self.conn.execute(
            "INSERT INTO facts(topic, concept, content, source, confidence) VALUES (?, ?, ?, ?, ?)",
            (topic, concept, content, source, confidence)
        )
        self.conn.commit()

    def store_theory(self, title, content):
        self.conn.execute(
            "INSERT INTO theories(title, content) VALUES (?, ?)",
            (title, content)
        )
        self.conn.commit()

    def save_chat(self, user_message, ai_message):
        self.conn.execute(
            "INSERT INTO chat_history(user_message, ai_message) VALUES (?, ?)",
            (user_message, ai_message)
        )
        self.conn.commit()

    def get_recent_chat(self, limit=10):
        rows = self.conn.execute("""
            SELECT user_message, ai_message
            FROM chat_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in rows]

    def search(self, query, limit=10):
        q = f"%{query.lower()}%"
        rows = self.conn.execute("""
            SELECT topic, concept, content, source, confidence
            FROM facts
            WHERE lower(topic) LIKE ? OR lower(concept) LIKE ? OR lower(content) LIKE ?
            ORDER BY confidence DESC
            LIMIT ?
        """, (q, q, q, limit)).fetchall()
        return [dict(r) for r in rows]

    def count(self):
        return self.conn.execute("SELECT COUNT(*) FROM facts").fetchone()[0]

    def concept_summary(self):
        return [dict(r) for r in self.conn.execute(
            "SELECT topic, COUNT(*) AS count FROM facts GROUP BY topic ORDER BY count DESC"
        ).fetchall()]

    def get_theories(self, limit=10):
        return [dict(r) for r in self.conn.execute(
            "SELECT title, content FROM theories ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()]
