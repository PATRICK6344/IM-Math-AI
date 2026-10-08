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
                eq = sp.Eq(sp.sympify(left), sp.sympify(right))
                return {
                    "equation": eq,
                    "solution": sp.solve(eq),
                }

            parsed = sp.sympify(expression)
            x = sp.Symbol("x")
            return {
                "expression": parsed,
                "derivative": sp.diff(parsed, x),
                "integral": sp.integrate(parsed, x),
            }
        except Exception as exc:
            return {"error": f"Unable to parse or solve: {exc}"}

    def explain(self, topic: str):
        topic = topic.lower().strip()
        topics = {
            "calculus": "Calculus studies change, limits, derivatives, and integrals. It formalizes how functions behave at points and across intervals.",
            "algebra": "Algebra studies symbolic structure, equations, transformations, and invariants under operations.",
            "topology": "Topology studies continuity and shape under deformation, without relying on exact metric distances.",
            "number_theory": "Number theory studies arithmetic properties of integers, primes, congruences, and divisibility.",
            "probability": "Probability studies uncertainty, distributions, expectation, variance, and stochastic behavior.",
            "geometry": "Geometry studies shape, distance, angles, symmetries, and spatial structures.",
            "analysis": "Analysis studies convergence, limits, compactness, measure, and the rigorous structure of continuous systems.",
            "general_math": "Advanced mathematics studies abstraction, proofs, structure, and the relation between symbolic forms and deeper conceptual systems.",
        }
        return topics.get(topic, topics["general_math"])

    def generate_quiz(self, topic: str = "calculus", count: int = 5):
        bank = {
            "calculus": [
                ("Derivative of x^3 + 2x", "3*x^2 + 2"),
                ("Integral of 2x", "x^2"),
                ("Derivative of sin(x)", "cos(x)"),
                ("Integral of e^x", "exp(x)"),
                ("Limit of (x^2 - 1)/(x - 1) as x -> 1", "2"),
            ],
            "algebra": [
                ("Solve x^2 - 5x + 6 = 0", "x = 2 or x = 3"),
                ("Expand (x + 2)^2", "x^2 + 4*x + 4"),
                ("Factor x^2 - 9", "(x - 3)*(x + 3)"),
                ("Simplify (x^2 - 1)/(x - 1)", "x + 1"),
                ("Solve 2x + 3 = 11", "x = 4"),
            ],
            "linear_algebra": [
                ("Determinant of [[2,0],[0,3]]", "6"),
                ("Trace of [[1,2],[3,4]]", "5"),
                ("Eigenvalues of [[1,0],[0,2]]", "1 and 2"),
            ],
            "number_theory": [
                ("Prime factorization of 60", "2^2 * 3 * 5"),
                ("GCD(48, 18)", "6"),
                ("Is 17 prime?", "Yes"),
            ],
        }
        return bank.get(topic.lower(), bank["calculus"])[:count]

    def infer_topic(self, text: str) -> str:
        lower = text.lower()
        if any(word in lower for word in ["derivative", "integral", "limit", "differential", "continuity"]):
            return "calculus"
        if any(word in lower for word in ["matrix", "vector", "polynomial", "equation", "group", "field"]):
            return "algebra"
        if any(word in lower for word in ["topology", "continuous", "compact", "manifold", "space"]):
            return "topology"
        if any(word in lower for word in ["prime", "modulo", "gcd", "divisibility", "integer"]):
            return "number_theory"
        if any(word in lower for word in ["probability", "random", "variance", "expectation"]):
            return "probability"
        if any(word in lower for word in ["triangle", "circle", "angle", "distance", "symmetry"]):
            return "geometry"
        return "general_math"

    def extract_keywords(self, text: str):
        words = re.findall(r"[A-Za-z][A-Za-z-]{2,}", text.lower())
        stop_words = {"the", "this", "that", "then", "with", "from", "into", "about", "more", "than", "there", "where", "when", "what", "which", "your", "have", "been", "would", "could", "should", "also", "using"}
        seen = set()
        result = []
        for w in words:
            if w in stop_words or len(w) < 3:
                continue
            if w not in seen:
                seen.add(w)
                result.append(w)
        return result[:8]
