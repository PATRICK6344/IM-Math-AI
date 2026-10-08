# IM Pro Max - Build and Release Guide

## Prerequisites
- Android Studio 2023.1+
- JDK 17
- Python 3.8+
- Git
- A Google Play Developer account

## Build Steps

### 1. Clone the repository
```bash
git clone https://github.com/PATRICK6344/IM-Math-AI.git
cd IM-Math-AI/android
```

### 2. Generate signing keystore
```bash
keytool -genkey -v -keystore im_keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 -alias im_key
```

### 3. Configure environment variables
```bash
export KEYSTORE_PASSWORD="your_password"
export KEY_ALIAS="im_key"
export KEY_PASSWORD="your_password"
```

### 4. Open in Android Studio
- Open `android` folder in Android Studio
- Sync Gradle
- Select Build > Generate Signed Bundle / APK
- Choose Android App Bundle (recommended for Play Store)
- Select release build type

### 5. Test locally
- Build APK for emulator/device
- Install and test thoroughly
- Verify model downloads
- Test all features: chat, solve, learn, theory

## Release Checklist

- [ ] Increment versionCode and versionName
- [ ] Update README.md if needed
- [ ] Verify all features work
- [ ] Test on multiple devices
- [ ] Build signed release bundle
- [ ] Create keystore backup
- [ ] Update CHANGELOG
- [ ] Tag release in Git

## Google Play Console Upload

1. Open Google Play Console
2. Create new app or select IM Pro Max
3. Go to Release > Production
4. Upload signed AAB
5. Fill in release notes
6. Submit for review

## App Listing Details

**Title**: IM Pro Max
**Subtitle**: Offline Mathematics AI
**Short Description**: Learn, solve, and explore mathematics locally on Android.

**Full Description**:
IM Pro Max is an offline mathematics AI that runs entirely on your Android device.

Features:
- Solve equations and symbolic expressions
- Explain mathematical concepts
- Generate mathematical ideas and conjectures
- Learn from local knowledge
- Run offline after initial setup
- Privacy-first design

**Category**: Education / Learning
**Content Rating**: For all ages
**Privacy Policy**: See PRIVACY_POLICY.md

## Screenshots for Play Store

Recommended screenshots:
1. Home screen with chat interface
2. Example equation solving
3. Theory generation
4. Explanation screen

## Model Selection

For optimal performance on Android:
- Recommended: Qwen2.5 3B or Llama 3.2 3B
- Good: Mistral 7B (if device has 6GB+ RAM)
- Model URL is set in IMService.java

## Troubleshooting

### Model download fails
- Check internet connection
- Verify storage space (requires ~7GB for Mistral)
- Check firewall/proxy settings

### App crashes on startup
- Ensure Python dependencies are installed
- Check logcat for errors
- Verify model path is correct

### Slow responses
- Model inference is CPU-bound
- This is expected; device will get warm
- 3B models are faster than 7B

## Versioning

Use semantic versioning:
- 1.0.0: Initial release
- 1.0.1: Bug fixes
- 1.1.0: Feature additions

## Support

Issues and feedback:
- GitHub: https://github.com/PATRICK6344/IM-Math-AI/issues
- Email: patrick.mihai.ple@gmail.com
