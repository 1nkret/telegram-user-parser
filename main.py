import threading
import asyncio
from app.gui import TelegramGUI

global_loop = asyncio.new_event_loop()


def start_async_loop():
    asyncio.set_event_loop(global_loop)
    global_loop.run_forever()


threading.Thread(target=start_async_loop, daemon=True).start()

app = TelegramGUI(global_loop)
app.mainloop()
