import os
import shutil
import sqlite3
from pathlib import Path


class ChromeIndexer:
    def __init__(self, knowledge):
        self.knowledge = knowledge

    def find_history_files(self):
        home = Path.home()
        candidates = [
            home / ".config" / "google-chrome" / "Default" / "History",
            home / ".config" / "chromium" / "Default" / "History",
            home / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "History",
            home / "AppData" / "Local" / "Chromium" / "User Data" / "Default" / "History",
        ]
        return [str(p) for p in candidates if p.exists()]

    def index(self):
        files = self.find_history_files()
        if not files:
            print("No Chrome history database found.")
            return []

        found = []
        for path in files:
            try:
                temp_copy = "chrome_history_tmp.db"
                shutil.copy2(path, temp_copy)
                conn = sqlite3.connect(temp_copy)
                rows = conn.execute(
                    "SELECT url, title FROM urls ORDER BY last_visit_time DESC LIMIT 200"
                ).fetchall()
                conn.close()
                os.remove(temp_copy)

                for url, title in rows:
                    text = f"{title or ''} {url or ''}".lower()
                    if any(word in text for word in ["math", "algebra", "integral", "derivative", "matrix", "topology", "prime", "probability"]):
                        self.knowledge.store_fact("web_math", title or "Math article", f"{title} - {url}", "chrome", 0.7)
                        found.append((title or url, "web_math"))
            except Exception as exc:
                print(f"Could not parse Chrome history: {exc}")
        return found
