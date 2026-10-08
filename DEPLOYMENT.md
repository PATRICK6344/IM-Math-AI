# IM Pro Max - Setup & Deployment

## Quick Start

### For Users
1. Download IM Pro Max from Google Play
2. Open the app
3. Wait for model to download (first run only)
4. Start chatting!

### For Developers

#### Clone and Setup
```bash
git clone https://github.com/PATRICK6344/IM-Math-AI.git
cd IM-Math-AI
```

#### Local Testing
```bash
# Install Python dependencies
pip install -r requirements.txt

# Test backend locally
python3 -c "from im_agent import chat_with_llm; print(chat_with_llm('Hello'))"
```

#### Android Build
```bash
cd android
./gradlew build              # Debug build
./gradlew assembleRelease    # Release build
./gradlew bundleRelease      # Play Store bundle
```

## Configuration

### Model Selection

Edit `IMService.java` line with model URL:

**For Mistral 7B (recommended):**
```java
String url = "https://huggingface.co/TheBloke/Mistral-7B-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf";
```

**For Qwen 3B (faster):**
```java
String url = "https://huggingface.co/second-state/qwen2.5-3b-instruct-gguf/resolve/main/qwen2.5-3b-instruct-q8_0.gguf";
```

**For Llama 3.2 3B (balanced):**
```java
String url = "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q8_0.gguf";
```

### Environment Setup

Create `.env` file (optional):
```
MODEL_PATH=/data/data/com.im.mathai/files/models/mistral.gguf
DB_PATH=/data/data/com.im.mathai/files/im_pro_max.db
LOG_LEVEL=INFO
```

## Deployment Pipeline

### GitHub Actions (optional)

Create `.github/workflows/android.yml`:
```yaml
name: Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-java@v2
        with:
          java-version: '17'
      - run: cd android && ./gradlew build
```

### Manual Release

1. Increment version in `build.gradle`
2. Update `CHANGELOG.md`
3. Build signed bundle:
   ```bash
   cd android
   ./gradlew bundleRelease
   ```
4. Upload to Play Console
5. Wait for review (typically 2-4 hours)
6. Tag release in Git:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

## Monitoring

### Key Metrics
- Install count
- Daily active users (DAU)
- Crash rate
- Average rating
- Retention rates

### Crash Tracking
- Monitor Play Console Vitals
- Check logcat for errors
- Review ANR (Application Not Responding) events

## Optimization

### For Performance
- Model inference is single-threaded
- Recommend 3B model for most devices
- 7B model works on 8GB+ RAM devices
- Initial startup: ~10 seconds
- Per-inference: ~2-3 seconds on average device

### For Storage
- Mistral 7B: ~7GB
- Qwen/Llama 3B: ~2-3GB
- Database: <10MB
- App APK: ~50MB (after download)

### For Battery
- Inference uses CPU heavily
- Avoid prolonged usage sessions
- Consider thermal management
- Background service not required

## Troubleshooting

### Build Issues
```bash
# Clean build
cd android && ./gradlew clean

# Update dependencies
./gradlew --refresh-dependencies

# Full rebuild
./gradlew clean bundleRelease
```

### Runtime Issues
- Check logcat: `adb logcat | grep IMService`
- Verify Python runtime: `adb shell pm dump com.im.mathai`
- Test model download manually
- Check disk space: `adb shell df`

### Model Loading
```python
# Test model loading
from llama_cpp import Llama
model = Llama(model_path="/path/to/model.gguf", n_threads=4)
response = model("Hello")
print(response)
```

## Security Considerations

- App runs entirely local (no server)
- No authentication required
- No analytics or telemetry
- ProGuard obfuscation enabled
- No sensitive data in logs
- Model files not encrypted (acceptable for offline)

## Future Considerations

1. **Model updates**: Plan for updatable models via app
2. **Multiple models**: Allow user selection
3. **Cloud optional**: Add optional cloud backup
4. **API**: Consider headless API mode
5. **Open source**: Plan public release on GitHub

## Support Channels

- GitHub Issues: Bug reports and feature requests
- Email: patrick.mihai.ple@gmail.com
- Play Store reviews: User feedback

## License

MIT License - See LICENSE file
