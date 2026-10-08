# IM Pro Max

Offline mathematics AI for Android, built to learn, reason, solve symbolic problems, and generate mathematical ideas locally on-device.

## Overview

IM Pro Max is a mobile mathematics assistant designed for students, learners, and enthusiasts who want a local AI that can:
- solve symbolic equations and algebraic expressions
- explain calculus, algebra, geometry, topology, and probability
- store knowledge locally on device
- generate new mathematical conjectures or theoretical directions
- work without internet after the initial model download

## Core capabilities

- Local AI chat using an on-device model
- Offline knowledge storage with SQLite
- Symbolic mathematics with SymPy
- Theory generation and conjecture drafting
- Mathematical explanations with topic-aware reasoning
- Fallback reasoning when the model is not available

## Architecture

- Android frontend in Java
- Python backend via Chaquopy
- Local SQLite memory
- SymPy symbolic engine
- Local GGUF model loading with llama.cpp
- Fallback logic for offline reliability

## Build and run

1. Open the project in Android Studio.
2. Sync Gradle.
3. Build the app for an emulator or physical Android device.
4. On first run, the app downloads the local AI model if it is not already present.
5. Once the model is downloaded, the app runs without requiring internet for most operations.

## Model behavior

The app stores the model in the local application folder, for example:

```text
/data/data/com.im.mathai/files/models/mistral.gguf
```

If the model is unavailable, the app automatically falls back to local symbolic reasoning and rule-based responses.

## Example commands

- Hello
- Solve x^2 - 5x + 6 = 0
- Explain calculus
- Generate theory
- Learn the derivative of x^n is n*x^(n-1)

## Project intent

This project is designed to be:
- offline first
- local and privacy-friendly
- educational and research-oriented
- suitable for Android deployment
- a basis for future AI-assisted mathematical exploration

## License

MIT

## Repository

GitHub: https://github.com/PATRICK6344/IM-Math-AI
