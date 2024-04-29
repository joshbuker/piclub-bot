"""
The main entrypoint to the bot
"""

import os

from dotenv import load_dotenv

# -------- Config --------
import config

# Load .env variables into environment
load_dotenv()

# Load configuration from environment
config.DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if config.DISCORD_TOKEN is None or config.DISCORD_TOKEN == "":
    print("Error: DISCORD_TOKEN must be set in environment")
    exit(1)

# The root directory should be the top level directory in this repo
config.ROOT_DIR = os.curdir

config.DATA_DIR = os.path.join(config.ROOT_DIR, config.DATA_DIR)

if not os.path.exists(config.DATA_DIR):
    os.mkdir(config.DATA_DIR) # Ensure data directory is present

config.DB_NAME = os.path.join(config.DATA_DIR, config.DB_NAME)
config.CONFIG_FILE = os.path.join(config.DATA_DIR, config.CONFIG_FILE)

# -------- Main --------

# Import internal modules that depend on configuration after changes
import bot # TODO: Why can't I do `from . import bot`?
#import bot.config as botcfg

#with open(config.CONFIG_FILE) as f:
    #botcfg.botconfig.load_from_file(f)


# Run bot
try:
    bot.client.run(config.DISCORD_TOKEN)
except KeyboardInterrupt:
    print("Ctrl-C") # Exit cleanly in case of a KeyboardInterrupt
