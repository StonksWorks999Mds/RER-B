#!/usr/bin/env python3
"""Rend l'appli Android compatible Android TV (icône sur l'écran d'accueil de la TV,
télécommande, sans écran tactile). L'APK reste installable sur téléphone."""
import re, shutil, sys, pathlib

root = pathlib.Path('android/app/src/main')
mf = root / 'AndroidManifest.xml'
s = mf.read_text(encoding='utf8')

if 'LEANBACK_LAUNCHER' in s:
    print('déjà adapté'); sys.exit(0)

# 1) catégorie de lancement Android TV
launcher = '<category android:name="android.intent.category.LAUNCHER" />'
assert launcher in s, 'catégorie LAUNCHER introuvable'
s = s.replace(launcher, launcher + '\n                <category android:name="android.intent.category.LEANBACK_LAUNCHER" />', 1)

# 2) bannière de l'application
assert '<application' in s, '<application> introuvable'
s = s.replace('<application', '<application\n        android:banner="@drawable/tv_banner"', 1)

# 3) pas d'écran tactile obligatoire + compatible TV
features = ('    <uses-feature android:name="android.software.leanback" android:required="false" />\n'
            '    <uses-feature android:name="android.hardware.touchscreen" android:required="false" />\n\n')
i = s.index('<application')
i = s.rfind('\n', 0, i) + 1
s = s[:i] + features + s[i:]
mf.write_text(s, encoding='utf8')

# 4) image de bannière (320x180 dp)
dst = root / 'res' / 'drawable-xhdpi'
dst.mkdir(parents=True, exist_ok=True)
shutil.copy('tv/tv_banner.png', dst / 'tv_banner.png')
print('AndroidManifest.xml adapté pour Android TV')
