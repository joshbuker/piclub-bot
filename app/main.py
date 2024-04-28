"""
The main entrypoint to the bot
"""

import os

from dotenv import load_dotenv

import bot # TODO: Why can't I do `from . import bot`?

# Load .env variables into environment
load_dotenv()

# Load configuration from environment
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None or TOKEN == "":
    print("Error: DISCORD_TOKEN must be set in environment")
    exit(1)

try:
    bot.client.run(TOKEN)
except KeyboardInterrupt:
    print("Ctrl-C") # Exit cleanly in case of a KeyboardInterrupt
