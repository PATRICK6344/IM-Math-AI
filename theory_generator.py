import random

class TheoryGenerator:
    def __init__(self, knowledge=None):
        self.knowledge = knowledge

    def generate(self, context=None):
        concepts = ["symmetry", "continuity", "matrix", "polynomial", "topology", "modularity", "duality", "measure"]
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
        rows = self.knowledge.search("", limit=10)
        concepts = []
        for row in rows:
            if row.get("concept"):
                concepts.append(row["concept"])
        if not concepts:
            return "A generalized theorem linking structure and continuity across symbolic systems."
        return self.generate(context=list(dict.fromkeys(concepts))[:6])
