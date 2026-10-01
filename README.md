# Lakshya

Personal goal tracker for Android by Faaz Dev Labs. Long-term goals, short-term goals, strategies, methods and tasks, each with a deadline and a live countdown. Urgency is colour-coded, tasks are ranked by what needs you most, reminders fire before deadlines, and every goal has a journal.

## Getting the app

Every push to `main` builds a new APK with GitHub Actions and publishes it under **Releases**. Download the latest `Lakshya-v1.0.x.apk` on your phone and open it to install. New versions install over the old one and keep your data, because every build is signed with the same key (`android/app/lakshya.keystore`). Keep this repository private.

## Where things live

- `www/index.html` — the whole app (screens, logic, animations)
- `www/fonts/` — fonts bundled for offline use
- `android/` — the Android project (icons, splash, signing)
- `.github/workflows/build.yml` — builds and publishes the APK
