from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': True,
    'includes': ['tkinter'],
    'packages': ['app'],
    'plist': {
        'CFBundleName': 'Telegram_Parser',
        'CFBundleDisplayName': 'Telegram Parser',
        'CFBundleIdentifier': 'com.example.telegram_parser',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True
    }
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
