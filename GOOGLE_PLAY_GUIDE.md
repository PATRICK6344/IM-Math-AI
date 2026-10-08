# Google Play Launch Guide for IM Pro Max

## 1. App overview

IM Pro Max is a mobile mathematics assistant for Android that can:
- solve equations and symbolic expressions
- explain mathematical topics
- generate theory ideas and conjectures
- run locally with a downloaded AI model
- operate offline after setup

## 2. Store category

Use:
- Category: Education
- Subcategory: Learning / Mathematics

## 3. App naming

Recommended title:
- IM Pro Max

Short description:
- Offline mathematics AI

## 4. App description for Play Store

IM Pro Max is an offline mathematics AI built for students, learners, and curious minds.

Learn, solve, and explore mathematics directly on your Android device.

Features:
- Solve equations and symbolic expressions
- Explain topics like calculus, algebra, geometry, topology, and probability
- Generate mathematical ideas and conjectures
- Use local AI inference with a downloaded model
- Run offline after the first setup
- Store knowledge locally on-device

This app is designed for mathematical learning, reasoning, and exploration without needing internet access for everyday use.

## 5. Privacy policy requirement

Google Play requires a clear privacy policy when the app includes storage or model downloads.

Use the included `PRIVACY_POLICY.md` file in this project.

## 6. Build checklist

Before publishing:
- [ ] Set the package name and signing key
- [ ] Build a signed Android App Bundle or APK
- [ ] Review permissions
- [ ] Confirm the app works offline after initial setup
- [ ] Check model download logic
- [ ] Add privacy policy URL
- [ ] Test on at least one Android device or emulator

## 7. Permissions

Recommended permissions:
- INTERNET
- ACCESS_NETWORK_STATE
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE

Explain in the Play listing that the app downloads the local model on first run and uses local storage for knowledge.

## 8. Versioning

Use semantic versioning:
- 1.0.0 initial release
- 1.0.1 bug fixes
- 1.1.0 functional improvements

## 9. App signing

Generate a keystore and sign the release build:

```bash
keytool -genkey -v -keystore im_keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias im_key
```

Then build the release bundle in Android Studio:
- Build > Generate Signed Bundle / APK

## 10. Upload to Google Play Console

1. Create or open a Google Play Developer account.
2. Create a new app in the Play Console.
3. Upload the signed Android App Bundle (AAB) or APK.
4. Fill in app details, screenshots, and description.
5. Add the privacy policy URL.
6. Submit for review.

## 11. Screenshots

Recommended screens:
- chat interface with AI conversation
- equation solving output
- theory generation output
- local model status screen
- help or math explanation screen

## 12. Notes for launch

This app is best positioned as an educational/offline AI product.
It should be presented as:
- AI-powered learning companion
- local mathematics assistant
- offline tool for exploration and study

## 13. First-release recommendation

For initial launch, keep scope focused on:
- solving equations
- chat responses
- educational explanations
- theory generation
- stability and offline functionality

Avoid overpromising advanced formal theorem proving in the first release.

## 14. Suggested title and slogan

Title: IM Pro Max
Slogan: Learn. Solve. Discover.
