from chrome_indexer import ChromeIndexer
from knowledge import KnowledgeBase
from math_core import MathCore
from theory_generator import TheoryGenerator
from wikipedia_loader import WikipediaLoader


class IMAgent:
    def __init__(self):
        self.memory = KnowledgeBase("im.db")
        self.math = MathCore()
        self.theory_gen = TheoryGenerator(knowledge=self.memory)
        self.chrome = ChromeIndexer(self.memory)
        self.wiki = WikipediaLoader(self.memory)
        self.boot()

    def boot(self):
        print("IM online. Offline mathematics engine is ready.")

    def run(self):
        print("Type 'help' to see commands.")
        while True:
            user_input = input("IM> ").strip()

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit", "bye"}:
                print("IM offline.")
                break

            if user_input.lower() == "help":
                print("""
Commands:
  learn <fact>
  solve <expression>
  theory
  quiz [topic]
  search <query>
  explain <topic>
  stats
  chrome
  wiki
  explore
  exit
""")
                continue

            if user_input.lower().startswith("learn "):
                fact = user_input[6:].strip()
                if not fact:
                    print("No fact provided.")
                    continue
                topic = self.math.infer_topic(fact)
                concept = self.math.extract_keywords(fact)[0] if self.math.extract_keywords(fact) else "general_math"
                self.memory.store_fact(topic, concept, fact, "manual", 0.8)
                print(f"Learned: {concept} ({topic})")
                continue

            if user_input.lower().startswith("solve "):
                expr = user_input[6:].strip()
                print(self.math.solve(expr))
                continue

            if user_input.lower() == "theory":
                theory = self.theory_gen.generate_from_memory()
                print("Generated theory:", theory)
                self.memory.store_theory("Generated theory", theory)
                continue

            if user_input.lower().startswith("quiz"):
                pieces = user_input.split()
                topic = pieces[1].lower() if len(pieces) > 1 else "calculus"
                questions = self.math.generate_quiz(topic=topic, count=5)
                for idx, (question, answer) in enumerate(questions, start=1):
                    print(f"{idx}. {question} -> {answer}")
                continue

            if user_input.lower().startswith("search "):
                query = user_input[7:].strip()
                results = self.memory.search(query, limit=10)
                if not results:
                    print("No matching knowledge found.")
                else:
                    for item in results:
                        print(f"- {item['concept']} | topic: {item['topic']} | confidence: {item['confidence']}")
                        print(f"  {item['content'][:180]}")
                continue

            if user_input.lower().startswith("explain "):
                topic = user_input[8:].strip()
                print(self.math.explain(topic))
                continue

            if user_input.lower() == "stats":
                total = self.memory.count()
                summary = self.memory.concept_summary()
                print(f"Knowledge items: {total}")
                for item in summary:
                    print(f"- {item['topic']}: {item['count']}")
                continue

            if user_input.lower() == "chrome":
                results = self.chrome.index()
                print(f"Indexed Chrome items: {len(results)}")
                continue

            if user_input.lower() == "wiki":
                results = self.wiki.load()
                print(f"Loaded Wikipedia entries: {len(results)}")
                continue

            if user_input.lower() == "explore":
                theory = self.theory_gen.generate_from_memory()
                print("Potential innovation:", theory)
                print("Recent theories:")
                for entry in self.memory.get_theories(limit=5):
                    print(f"- {entry['title']}: {entry['content']}")
                continue

            # default: learn and respond conversationally
            topic = self.math.infer_topic(user_input)
            concept = self.math.extract_keywords(user_input)[0] if self.math.extract_keywords(user_input) else "general_concept"
            self.memory.store_fact(topic, concept, user_input, "conversation", 0.65)
            print("I have stored this in memory and can reason from it later.")
            print("I can also solve equations, generate theories, or explain the topic.")
