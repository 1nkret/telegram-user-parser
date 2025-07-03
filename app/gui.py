import tkinter as tk
from tkinter import ttk, messagebox
import asyncio

from telethon import TelegramClient

from app.config_manager import load_config, save_config
from app.gui_utils import code_input_dialog, password_input_dialog
from app.telegram import auth_with_password, get_admin_channels, get_session_path
from app.save_csv import save_users_to_csv
from app.telegram import get_users_from_channel


class TelegramGUI(tk.Tk):
    def __init__(self, passed_loop):
        super().__init__()
        self.loop = passed_loop
        self.title("Telegram Parser")
        self.geometry("420x300")
        self.resizable(False, False)

        self.shared_data = load_config()
        self.client = None
        self.channel_list = []

        self.page1_frame = None
        self.page2_frame = None

        self.after(100, self.startup_flow)

    def startup_flow(self):
        async def startup():
            if await self.check_existing_session():
                self.after(0, self.build_page2)
            else:
                self.after(0, self.build_page1)

        asyncio.run_coroutine_threadsafe(startup(), self.loop)

    async def check_existing_session_and_build_pages(self):
        if await self.check_existing_session():
            self.build_page2()
        else:
            self.build_page1()

    def build_page1(self):
        if self.page2_frame:
            self.page2_frame.destroy()

        self.page1_frame = ttk.Frame(self)
        self.page1_frame.pack(fill="both", expand=True)

        ttk.Label(self.page1_frame, text="API_ID:").pack(pady=(10, 0))
        self.api_id_entry = ttk.Entry(self.page1_frame)
        self.api_id_entry.insert(0, self.shared_data.get("api_id", ""))
        self.api_id_entry.pack()

        ttk.Label(self.page1_frame, text="API_HASH:").pack(pady=(10, 0))
        self.api_hash_entry = ttk.Entry(self.page1_frame)
        self.api_hash_entry.insert(0, self.shared_data.get("api_hash", ""))
        self.api_hash_entry.pack()

        ttk.Label(self.page1_frame, text="PHONE:").pack(pady=(10, 0))
        self.phone_entry = ttk.Entry(self.page1_frame)
        self.phone_entry.insert(0, self.shared_data.get("phone", ""))
        self.phone_entry.pack()

        ttk.Label(self.page1_frame, text="PASSWORD:").pack(pady=(10, 0))
        self.password_entry = ttk.Entry(self.page1_frame, show="*")
        self.password_entry.insert(0, self.shared_data.get("password", ""))
        self.password_entry.pack()

        self.login_btn = ttk.Button(self.page1_frame, text="Войти", command=self.try_login)
        self.login_btn.pack(pady=15)

    def try_login(self):
        try:
            api_id = int(self.api_id_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "API_ID должен быть числом.")
            return

        api_hash = self.api_hash_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()

        self.shared_data = {
            "api_id": str(api_id),
            "api_hash": api_hash,
            "phone": phone,
            "password": password
        }
        save_config(self.shared_data)

        async def do_login():
            try:
                self.client = await auth_with_password(
                    session_name="channel_parser",
                    api_id=api_id,
                    api_hash=api_hash,
                    phone=phone,
                    password=password,
                    get_code_func=code_input_dialog,
                    get_password_func=password_input_dialog
                )
                self.channel_list = await get_admin_channels(self.client)
                self.after(0, self.build_page2)
            except Exception as e:
                self.after(0, lambda err=e: messagebox.showerror("Ошибка", str(err)))

        asyncio.run_coroutine_threadsafe(do_login(), self.loop)

    def build_page2(self):
        if self.page1_frame:
            self.page1_frame.destroy()

        self.page2_frame = ttk.Frame(self)
        self.page2_frame.pack(fill="both", expand=True)

        ttk.Label(self.page2_frame, text="Выберите канал:").pack(pady=(15, 5))

        self.channel_list.sort()
        self.channel_var = tk.StringVar()
        self.channel_combo = ttk.Combobox(self.page2_frame, textvariable=self.channel_var, values=self.channel_list, state="readonly", width=50)
        self.channel_combo.pack()

        ttk.Button(self.page2_frame, text="Собрать участников", command=self.download_users).pack(pady=20)

    def download_users(self):
        selected_channel = self.channel_var.get()
        if not selected_channel:
            messagebox.showwarning("Внимание", "Выберите канал из списка.")
            return

        async def fetch_and_save():
            users = await get_users_from_channel(self.client, selected_channel)
            save_users_to_csv(users)
            self.after(0, lambda: messagebox.showinfo("Готово", f"Сохранено {len(users)} пользователей."))

        asyncio.run_coroutine_threadsafe(fetch_and_save(), self.loop)

    async def check_existing_session(self):
        try:
            api_id = int(self.shared_data.get("api_id", ""))
            api_hash = self.shared_data.get("api_hash", "")
            phone = self.shared_data.get("phone", "")

            if not api_id or not api_hash or not phone:
                return False

            session_path = get_session_path()
            print("🟡 Checking session at:", session_path)

            self.client = TelegramClient(session_path, api_id, api_hash)
            await self.client.connect()

            authorized = await self.client.is_user_authorized()
            print("✅ Already authorized:", authorized)

            if authorized:
                self.channel_list = await get_admin_channels(self.client)
                return True

            return False
        except Exception as e:
            print("❌ Session check failed:", e)
            return False

