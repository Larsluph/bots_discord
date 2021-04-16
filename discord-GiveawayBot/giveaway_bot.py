#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import random
import time

import discord
import requests


class MyClient(discord.Client):
  baseurl = "https://discord.com/api"
  token = os.environ.get('GiveawayBot')
  prefix = "g!"

  def __enter__(self):
    self.run(self.token)

  def __exit__(self, exc_type, exc_value, traceback):
    print(f"[EXIT] {exc_type}: {exc_value}, {traceback}")
    return True

  async def on_connect(self):
    print('[LOGS] Connecting to discord!')

  async def on_ready(self):
    print('[LOGS] Bot is ready!')
    print(f"[LOGS] Logged in: {self.user.name}\n[LOGS] ID: {self.user.id}\n[LOGS] Number of users: {len(set(self.get_all_members()))}")
    await self.change_presence(status=discord.Status.online, activity=discord.Game(name="with the API"))

  async def on_resumed(self):
    print("\n[LOGS] Bot has resumed session!")

  async def on_message(self, message):
    if message.author == self.user: # don't respond to ourselves
      return

    elif message.content.startswith(self.prefix):
      if message.author == self.get_user(292714635394809876):
        if message.content[len(self.prefix):] == "start":
          await new_giveaway(message)

        elif message.content == 'logout':
          await message.channel.send("Disconnecting...")
          await self.close()
          print("[LOGS] Connection terminated")

        else:
          await self.hello(message)

    else:
      await self.hello(message)

  async def hello(self, message):
    await message.channel.send(f"Hello <@{message.author.id}> !")
    return

  async def new_giveaway(self, message):
    host_user = message.author.id
    args = message.content.split(" ")[1:]
    if len(args) != 2:
      await message.channel.send("Invalid command")
      return
    else:
      duration = int(args[0])
      prize = args[1]
      await message.channel.send(f"""\
        **NEW GIVEAWAY !**
        ```
        {prize}
        Giveaway Duration: {duration} minutes
        Hosted by: <@{host_user}>
        ```""")
      # react
      for i in range(duration*2):
        time.sleep(30)
        # edit countdown
      # check reactions
      # chose random winner
      # congrats !

if __name__ == "__main__":
  with MyClient() as client:
    pass
