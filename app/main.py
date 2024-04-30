"""
The main entrypoint to the bot
"""

import os

from dotenv import load_dotenv

# -------- Config --------
import globalconf

# Load .env variables into environment
load_dotenv()

# Load configuration from environment
globalconf.DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if globalconf.DISCORD_TOKEN is None or globalconf.DISCORD_TOKEN == "":
    print("Error: DISCORD_TOKEN must be set in environment")
    exit(1)

# The root directory should be the top level directory in this repo
globalconf.ROOT_DIR = os.curdir

print(f"ROOT_DIR: {os.path.abspath(globalconf.ROOT_DIR)}")

globalconf.DATA_DIR = os.path.join(globalconf.ROOT_DIR, globalconf.DATA_DIR)

print(f"DATA_DIR: {os.path.abspath(globalconf.DATA_DIR)}")

if not os.path.exists(globalconf.DATA_DIR):
    os.mkdir(globalconf.DATA_DIR) # Ensure data directory is present

globalconf.DB_FILE = os.path.join(globalconf.DATA_DIR, globalconf.DB_FILE)
print(f"DB_FILE: {os.path.abspath(globalconf.DB_FILE)}")

globalconf.CONFIG_FILE = os.path.join(globalconf.DATA_DIR, globalconf.CONFIG_FILE)
print(f"CONFIG_FILE: {os.path.abspath(globalconf.CONFIG_FILE)}")

# Create file if it doesn't exist
if not os.path.exists(globalconf.CONFIG_FILE):
    print(f"file doesn't exist: {globalconf.CONFIG_FILE}, creating...")
    open(globalconf.CONFIG_FILE, "a")

# LLM Config
llm_model = os.getenv("LLM_MODEL")
if not llm_model is None:
    globalconf.LLM_MODEL = llm_model

llm_host = os.getenv("LLM_HOST")
if not llm_host is None:
    globalconf.LLM_HOST = llm_host

llm_port = os.getenv("LLM_PORT")
if not llm_port is None:
    globalconf.LLM_PORT = llm_port

print("LLM:")
print(f"Model: {globalconf.LLM_MODEL}")
print(f"Host: {globalconf.LLM_HOST}")
print(f"Port: {globalconf.LLM_PORT}")

# -------- Main --------

# Import internal modules that depend on configuration after changes
import bot # TODO: Why can't I do `from . import bot`?
from bot import botconf

with open(globalconf.CONFIG_FILE, "r") as f:
    botconf.botconfig.load_from_file(f)

# Run bot
try:
    bot.client.run(globalconf.DISCORD_TOKEN)
except KeyboardInterrupt:
    print("Ctrl-C") # Exit cleanly in case of a KeyboardInterrupt
