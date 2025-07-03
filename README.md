# Telegram Channel Members Parser

A utility for extracting the full list of members from a Telegram channel or supergroup using your Telegram account via a graphical user interface (GUI).

---

## 🔧 Features

- Login via phone number, with support for 2FA (if enabled)
- Telegram session support (no need to log in every time)
- Channel selection where you are the **owner or an admin**
- Extract user information:
  - `username`
  - `first_name`
  - `last_name`
  - `phone` (if available)
- Save results to a `.csv` file

---

## ⚠️ Important

- To get the **full** list of members, you must be the **owner or an admin** of the channel.
- Telegram limits access to full member lists for regular users and non-privileged admins.
- You will need `api_id` and `api_hash`, which can be obtained at [my.telegram.org](https://my.telegram.org).

---

## 📦 Project Structure

```
app/
├── config_manager.py   # Configuration manager (API ID, HASH, phone, etc.)
├── gui.py              # Main GUI interface
├── gui_utils.py        # Dialogs for entering code and password
├── run.py              # Asyncio loop runner for the GUI
├── save_csv.py         # CSV export functionality
├── schemas.py          # TelegramUserInfo dataclass
├── telegram.py         # Auth and user parsing logic
main.py
README.md
requirements.txt
```

---

## ✅ Installation & Usage

### 1. Install Python and dependencies

Make sure you have **Python 3.13** installed.  
Then install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run the app

Start the application with:

```bash
python main.py
```

On first launch, a Telegram login window will appear. After successful login, you’ll be able to select a channel and save its members to a CSV file.

---

### 📂 Where is data stored?

All parameters (API ID, Hash, Phone, etc.) are saved automatically in a config file.  
The Telegram client session is also stored — no need to log in again each time.

---

### 📦 Prebuilt Versions

Precompiled `.exe` builds of this tool are available in the [Releases section](https://github.com/1nkret/telegram-user-parser/releases).  
No Python installation is required — just download and run.
