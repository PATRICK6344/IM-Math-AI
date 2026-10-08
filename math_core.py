import re
import sympy as sp

class MathCore:
    def solve(self, expression: str):
        expression = expression.strip()
        if not expression:
            return "No expression provided."

        try:
            if "=" in expression:
                left, right = [part.strip() for part in expression.split("=", 1)]
                equation = sp.Eq(sp.sympify(left), sp.sympify(right))
                return {
                    "equation": equation,
                    "solution": sp.solve(equation)
                }

            expr = sp.sympify(expression)
            x = sp.Symbol("x")
            return {
                "expression": expr,
                "derivative": sp.diff(expr, x),
                "integral": sp.integrate(expr, x)
            }
        except Exception as exc:
            return {"error": str(exc)}

    def explain(self, topic):
        topic = topic.lower().strip()
        data = {
            "calculus": "Calculus studies change, limits, derivatives, and integrals. It formalizes how quantities evolve over time or space.",
            "algebra": "Algebra studies symbolic manipulation, equations, and structures such as groups, matrices, and polynomials.",
            "topology": "Topology studies continuity and the shape of spaces under deformation, without depending on exact distances.",
            "number_theory": "Number theory studies integers, primes, divisibility, modular arithmetic, and deep arithmetic structure.",
            "probability": "Probability studies uncertainty using expectation, variance, distributions, and random variables.",
            "geometry": "Geometry studies distances, angles, congruence, symmetry, and spatial relationships.",
            "analysis": "Analysis studies limits, continuity, convergence, compactness, and measure.",
            "general_math": "Advanced mathematics studies abstraction, proof, structure, and relationships among mathematical ideas."
        }
        return data.get(topic, data["general_math"])

    def infer_topic(self, text: str) -> str:
        lower = text.lower()
        if any(w in lower for w in ["derivative", "integral", "limit", "differential", "continuity"]):
            return "calculus"
        if any(w in lower for w in ["matrix", "vector", "polynomial", "equation", "group", "field"]):
            return "algebra"
        if any(w in lower for w in ["topology", "continuous", "space", "manifold"]):
            return "topology"
        if any(w in lower for w in ["prime", "modulo", "gcd", "divisibility", "integer"]):
            return "number_theory"
        if any(w in lower for w in ["probability", "random", "variance", "expectation"]):
            return "probability"
        if any(w in lower for w in ["triangle", "circle", "angle", "distance", "symmetry"]):
            return "geometry"
        return "general_math"

    def extract_keywords(self, text):
        words = re.findall(r"[A-Za-z][A-Za-z-]{2,}", text.lower())
        stop_words = {"the", "this", "that", "then", "with", "from", "into", "about", "more", "than", "there", "where", "when", "what", "which", "your", "have", "been", "would", "could", "should", "also", "using"}
        seen = set()
        result = []
        for w in words:
            if w in stop_words or len(w) < 3:
                continue
            if w not in seen:
                result.append(w)
                seen.add(w)
            if len(result) >= 8:
                break
        return result
