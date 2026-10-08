# IM

IM is an offline self-learning mathematics AI designed to learn from local knowledge, reason with symbolic systems, explore mathematical structures, and propose new conjectures and theories.

## What it does
- Stores mathematical knowledge locally in SQLite
- Understands and solves symbolic equations with SymPy
- Generates mathematical conjectures based on local concepts
- Can read local Wikipedia text files and Chrome history if available
- Converses with the user in a terminal interface

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Example commands
- `learn The derivative of x^3 is 3x^2.`
- `solve x^2 - 5x + 6 = 0`
- `theory`
- `quiz`
- `search topology`
- `explain calculus`
- `stats`
- `exit`

## Project structure
- `agent.py` – interactive AI agent
- `knowledge.py` – local memory and concept graph
- `math_core.py` – symbolic reasoning and math tools
- `theory_generator.py` – conjecture and theory generation
- `chrome_indexer.py` – optional Chrome indexing
- `wikipedia_loader.py` – optional local Wikipedia indexing
- `main.py` – application entry point
