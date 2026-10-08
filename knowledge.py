import sqlite3
import re
from typing import List, Dict, Any


class KnowledgeBase:
    def __init__(self, db_path: str = "im.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.init_db()
        self.bootstrap_seed()

    def init_db(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS concepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                concept TEXT,
                content TEXT,
                source TEXT,
                confidence REAL DEFAULT 0.5,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_concept TEXT,
                target_concept TEXT,
                relation TEXT,
                weight REAL DEFAULT 0.5,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS theories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def bootstrap_seed(self):
        seed_items = [
            ("calculus", "derivative", "The derivative measures instantaneous change.", "seed", 0.95),
            ("calculus", "integral", "The integral accumulates quantities over a domain.", "seed", 0.95),
            ("algebra", "polynomial", "A polynomial is an expression of variables with coefficients.", "seed", 0.95),
            ("algebra", "matrix", "A matrix is a rectangular array of numbers or symbols.", "seed", 0.95),
            ("topology", "continuity", "Continuity means nearby points remain nearby.", "seed", 0.95),
            ("probability", "expectation", "Expectation is the average value of a random variable.", "seed", 0.95),
            ("number_theory", "prime", "A prime number has exactly two positive divisors.", "seed", 0.95),
            ("geometry", "symmetry", "Symmetry means invariance under a transformation.", "seed", 0.95),
        ]
        for item in seed_items:
            if not self.exists(item[1], item[0], item[2]):
                self.store_fact(*item)

    def exists(self, concept: str, topic: str, content: str) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM concepts WHERE concept = ? AND topic = ? AND content = ? LIMIT 1",
            (concept, topic, content),
        ).fetchone()
        return row is not None

    def store_fact(self, topic: str, concept: str, content: str, source: str, confidence: float = 0.7):
        concept = concept.strip()
        content = content.strip()
        if not concept or not content:
            return
        self.conn.execute(
            "INSERT INTO concepts(topic, concept, content, source, confidence) VALUES (?, ?, ?, ?, ?)",
            (topic, concept, content, source, confidence),
        )
        self.conn.commit()

    def store_relation(self, source_concept: str, target_concept: str, relation: str, weight: float = 0.5):
        if not source_concept or not target_concept:
            return
        self.conn.execute(
            "INSERT INTO relations(source_concept, target_concept, relation, weight) VALUES (?, ?, ?, ?)",
            (source_concept, target_concept, relation, weight),
        )
        self.conn.commit()

    def store_theory(self, title: str, content: str):
        if not title or not content:
            return
        self.conn.execute(
            "INSERT INTO theories(title, content) VALUES (?, ?)",
            (title, content),
        )
        self.conn.commit()

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        q = f"%{query.lower()}%"
        rows = self.conn.execute(
            """
            SELECT topic, concept, content, source, confidence
            FROM concepts
            WHERE lower(topic) LIKE ? OR lower(concept) LIKE ? OR lower(content) LIKE ?
            ORDER BY confidence DESC, created_at DESC
            LIMIT ?
            """,
            (q, q, q, limit),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_topics(self):
        rows = self.conn.execute("SELECT DISTINCT topic FROM concepts ORDER BY topic").fetchall()
        return [r[0] for r in rows]

    def get_related(self, concept: str, limit: int = 5):
        rows = self.conn.execute(
            """
            SELECT target_concept, relation, weight
            FROM relations
            WHERE source_concept = ?
            ORDER BY weight DESC
            LIMIT ?
            """,
            (concept, limit),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_theories(self, limit: int = 10):
        rows = self.conn.execute(
            "SELECT title, content FROM theories ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

    def count(self):
        row = self.conn.execute("SELECT COUNT(*) FROM concepts").fetchone()
        return row[0]

    def concept_summary(self):
        rows = self.conn.execute(
            "SELECT topic, COUNT(*) as count FROM concepts GROUP BY topic ORDER BY count DESC"
        ).fetchall()
        return [dict(r) for r in rows]

    def infer_concepts(self, text: str):
        text = text.lower()
        candidates = re.findall(r"[a-zA-Z][a-zA-Z-]{2,}", text)
        # Remove boilerplate words
        stop_words = {
            "the", "this", "that", "then", "with", "from", "into", "about", "more", "than",
            "there", "where", "when", "what", "which", "your", "have", "been", "would",
            "could", "should", "also", "using", "through", "because", "after", "before"
        }
        seen = set()
        result = []
        for w in candidates:
            if w in stop_words or len(w) < 3:
                continue
            if w not in seen:
                seen.add(w)
                result.append(w)
        return result[:8]
