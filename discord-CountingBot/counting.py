import os
import sys

import discord


class CountingBot(discord.Client):
    baseurl = "https://discord.com/api"
    token = os.environ.get("CountingBot")

    def __enter__(self):
        self.run(self.token)

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"[EXIT] {exc_type}: {exc_value}, {traceback}")
        return True

    async def on_ready(self):
        print('[LOGS] Bot is ready!')
        print(f"[LOGS] Logged in: {self.user.name}\n[LOGS] ID: {self.user.id}\n[LOGS] Number of users: {len(set(self.get_all_members()))}")

    async def on_resumed(self):
        print("\n[LOGS] Bot has resumed session!")

with CountingBot() as bot:
    pass
