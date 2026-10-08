from pathlib import Path


class WikipediaLoader:
    def __init__(self, knowledge, base_dir: str = "wikipedia_cache"):
        self.knowledge = knowledge
        self.base_dir = Path(base_dir)

    def load(self):
        if not self.base_dir.exists():
            print("No wikipedia_cache directory found.")
            return []

        loaded = []
        for file_path in sorted(self.base_dir.iterdir()):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in {".txt", ".md", ".html"}:
                continue

            try:
                text = file_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            if len(text) < 50:
                continue

            title = file_path.stem.replace("_", " ").replace("-", " ").title()
            self.knowledge.store_fact(
                "wikipedia",
                title,
                text[:600],
                str(file_path),
                0.9,
            )
            loaded.append(title)

        return loaded
