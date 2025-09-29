import logging
import logging.config
from datetime import datetime, date
import os
import sys
import asyncio
import pytz

import tgcrypto
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from pyrogram import utils as pyroutils
from aiohttp import web as webserver

from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR, LOG_CHANNEL
from utils import temp
from Script import script
from plugins.webcode import bot_run
from typing import Union, Optional, AsyncGenerator
from pyrogram import types

# Logging setup
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.CRITICAL - 1)

# Fix peer id invalid errors
pyroutils.MIN_CHAT_ID = -999999999999
pyroutils.MIN_CHANNEL_ID = -100999999999999

PORT_CODE = int(os.environ.get("PORT", "8080"))  # Replit default port

# -------------------- Bot Class --------------------
class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        # Load banned users & chats
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats

        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username

        logging.info(f"{me.first_name} with Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        logging.info(LOG_STR)

        # Send restart message to log channel
        await self.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT)
        tz = pytz.timezone('Asia/Kolkata')
        today = date.today()
        now = datetime.now(tz)
        time = now.strftime("%H:%M:%S %p")
        await self.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_GC_TXT.format(today, time))
        print("Safin's Bot is online ✅")

        # Start Flask-like server for UptimeRobot
        app_runner = webserver.AppRunner(await bot_run())
        await app_runner.setup()
        site = webserver.TCPSite(app_runner, "0.0.0.0", PORT_CODE)
        await site.start()
        logging.info(f"Web server running on port {PORT_CODE}")

        # Schedule auto-restart every 24 hours
        asyncio.create_task(self.schedule_restart())

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")

    # 24-hour auto-restart
    async def restart(self):
        logging.info("Restarting bot process...")
        await self.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    async def schedule_restart(self, hours: int = 24):
        await asyncio.sleep(hours * 60 * 60)
        await self.send_message(chat_id=LOG_CHANNEL, text="Auto Restarting the Bot \n(24 hrs ⏰️ refresh)...")
        await self.restart()

    # Iterator helper function (unchanged)
    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current + new_diff + 1)))
            for message in messages:
                yield message
                current += 1

# -------------------- Run Bot --------------------
app = Bot()
app.run()
