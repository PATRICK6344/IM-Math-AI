import os
from pathlib import Path

try:
    from llama_cpp import Llama
except Exception:
    Llama = None

from knowledge import KnowledgeBase
from math_core import MathCore
from theory_generator import TheoryGenerator

memory = KnowledgeBase("im_pro_max.db")
math_core = MathCore()
theory_gen = TheoryGenerator(knowledge=memory)

SYSTEM_PROMPT = """
You are IM Pro Max, an advanced mathematics AI.
You solve symbolic math problems carefully and explain concepts clearly.
When the user asks for a theorem, conjecture, or idea, generate a mathematically meaningful theory.
Prefer precise mathematical reasoning and exact symbolic methods.
If uncertainty exists, say so and suggest the next valid step.
"""

class LocalLLM:
    def __init__(self, model_path=None):
        self.model_path = model_path or str(Path.home() / "files" / "models" / "mistral.gguf")
        self.model = None
        self.available = False
        self.initialize()

    def initialize(self):
        if not os.path.exists(self.model_path):
            print(f"[IM] Model not found: {self.model_path}")
            self.available = False
            return

        if Llama is None:
            print("[IM] llama-cpp-python missing")
            self.available = False
            return

        try:
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=2048,
                n_threads=4,
                n_gpu_layers=0,
                verbose=False
            )
            self.available = True
            print("[IM] Local model loaded")
        except Exception as e:
            print(f"[IM] Failed to load model: {e}")
            self.available = False

    def generate(self, prompt: str, max_tokens: int = 400) -> str:
        if not self.available or self.model is None:
            return None
        try:
            result = self.model(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9,
                stop=["User:", "IM:"]
            )
            return result.get("choices", [{}])[0].get("text", "").strip()
        except Exception as e:
            print(f"[IM] Generation error: {e}")
            return None

llm = LocalLLM()

def fallback_chat(user_message: str) -> str:
    user_message = user_message.strip()
    if not user_message:
        return "Please type a message."

    topic = math_core.infer_topic(user_message)
    keywords = math_core.extract_keywords(user_message)
    concept = keywords[0] if keywords else "general_concept"

    memory.store_fact(topic, concept, user_message, "chat", 0.7)

    lower = user_message.lower()
    if any(w in lower for w in ["hello", "hi", "hey"]):
        return "Hello! I am IM Pro Max. I can solve equations, explain concepts, and generate theories."
    if any(w in lower for w in ["solve", "equation", "calculate"]):
        return "Try: solve x^2 - 5x + 6 = 0"
    if any(w in lower for w in ["theory", "conjecture", "discover"]):
        return "New direction: " + theory_gen.generate_from_memory()
    if any(w in lower for w in ["explain", "what is", "how does"]):
        topic_word = lower.replace("explain", "").replace("what is", "").replace("how does", "").strip()
        if not topic_word:
            topic_word = "calculus"
        return math_core.explain(topic_word)
    return "I have stored this in memory. Ask me to solve, explain, or generate a theory."

def initialize_llm(model_path: str = None):
    global llm
    llm = LocalLLM(model_path)
    return "Model initialized" if llm.available else "Model unavailable"

def learn(fact: str) -> str:
    fact = fact.strip()
    if not fact:
        return "Empty fact."
    topic = math_core.infer_topic(fact)
    keywords = math_core.extract_keywords(fact)
    concept = keywords[0] if keywords else "general_concept"
    memory.store_fact(topic, concept, fact, "manual", 0.85)
    return f"Learned: {concept} ({topic})"

def solve(equation: str) -> str:
    equation = equation.strip()
    if not equation:
        return "No equation provided."
    result = math_core.solve(equation)
    if isinstance(result, dict) and "error" in result:
        return result["error"]
    return str(result)

def generate_theory() -> str:
    theory = theory_gen.generate_from_memory()
    memory.store_theory("Generated (Android)", theory)
    return theory

def chat_with_llm(user_message: str) -> str:
    user_message = user_message.strip()
    if not user_message:
        return "Please type a message."

    if not llm.available:
        return fallback_chat(user_message)

    history = memory.get_recent_chat(limit=6)
    memory_text = ""
    if history:
        memory_text = "\n".join(
            f"- User: {item['user_message']}\n  AI: {item['ai_message'][:160]}"
            for item in history
            if item.get("user_message") and item.get("ai_message")
        )

    related = memory.search(user_message, limit=6)
    memory_related = ""
    if related:
        memory_related = "\n".join(
            f"- {row['concept']} ({row['topic']}): {row['content'][:160]}"
            for row in related if row.get("content")
        )

    prompt = f"""
{SYSTEM_PROMPT}

Relevant conversation memory:
{memory_text}

Relevant mathematical memory:
{memory_related}

User question:
{user_message}

Provide a clear, mathematically grounded response.
"""

    response = llm.generate(prompt, max_tokens=400)
    if response:
        memory.save_chat(user_message, response)
        return response.strip()

    return fallback_chat(user_message)

def process_command(command: str) -> str:
    cmd = command.strip()
    if not cmd:
        return "No command"
    lower = cmd.lower()

    if lower.startswith("learn "):
        return learn(cmd[6:])
    if lower.startswith("solve "):
        return solve(cmd[6:])
    if lower in ["theory", "generate theory"]:
        return generate_theory()
    if lower.startswith("chat "):
        return chat_with_llm(cmd[5:])
    if lower.startswith("explain "):
        return math_core.explain(cmd[8:])
    if lower.startswith("search "):
        results = memory.search(cmd[7:], limit=5)
        if not results:
            return "No results found."
        return "\n".join(f"{r['concept']} ({r['topic']})" for r in results)
    return chat_with_llm(cmd)
