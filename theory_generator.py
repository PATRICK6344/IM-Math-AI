import random


class TheoryGenerator:
    def __init__(self, knowledge=None):
        self.knowledge = knowledge

    def generate(self, context=None):
        concepts = [
            "symmetry",
            "continuity",
            "polynomial",
            "matrix",
            "topology",
            "modularity",
            "measure",
            "duality",
            "invariance",
            "dynamics",
        ]
        if context and isinstance(context, list):
            concepts = context[:6]

        a, b, c = random.sample(concepts, 3)
        templates = [
            f"A new invariant linking {a} and {b} under the action of {c}.",
            f"A generalized theorem stating that any structure preserving {a} also preserves {b} under {c}.",
            f"A conjectural bridge between {a} and {b} mediated by {c}.",
            f"A duality principle: every {a}-like object induces a canonical {b}-like object under {c}.",
        ]
        return random.choice(templates)

    def generate_from_memory(self):
        if self.knowledge is None:
            return "No memory available."
        topics = self.knowledge.get_topics()
        if not topics:
            return "No concepts available."

        # Build a lightweight concept pool
        pool = []
        for topic in topics:
            rows = self.knowledge.search(topic, limit=3)
            for row in rows:
                pool.append(row["concept"])

        if not pool:
            return "No concepts available."

        context = list(dict.fromkeys(pool))[:6]
        return self.generate(context=context)
