# Changelog

## [1.0.0] - 2026-10-08

### Features
- Offline mathematics AI with local model support
- Chat interface with real-time responses
- Symbolic equation solving via SymPy
- Mathematical concept explanations
- Theory and conjecture generation
- Local SQLite memory for learning
- Fallback logic when model unavailable
- Dark theme optimized UI
- Model auto-download on first run

### Technical
- Python 3.11 backend via Chaquopy
- llama.cpp for local model inference
- Android API 28+ support
- Arm64 and ARMv7 architecture support
- ProGuard minification and obfuscation

### Performance
- ~2-3 second responses on modern devices
- Model loading time: ~5-10 seconds
- Initial download: ~7GB for Mistral 7B

### Known Limitations
- Model download requires internet and storage
- Inference is CPU-bound (may make device warm)
- Best on devices with 6GB+ RAM
- 3B models recommended for lower-end devices

## Future Releases

### v1.1.0
- Model selection in app settings
- Conversation export
- Voice input support
- Advanced settings panel

### v2.0.0
- Multi-language support
- Cloud backup option
- Formal theorem proving
- Advanced visualization
