import random

import discord

from . import botconf as _botconf
from . import llm

_intents = discord.Intents.default()
_intents.message_content = True

client = discord.Client(intents=_intents)

def _is_command(text: str) -> bool:
    return text.startswith(_botconf.botconfig.command_prefix)


def _is_greeting(message: discord.Message) -> bool:
    has_greeting_prefix = False
    for greeting in _botconf.botconfig.greetings:
        if message.content.lower().startswith(greeting):
            has_greeting_prefix = True
            break

    if not has_greeting_prefix:
        return False

    return client.user in message.mentions


async def _handle_command(command: str, args: list[str], message: discord.Message):
    response = ""
    pre = _botconf.botconfig.command_prefix
    match command.lower():
        case "help" | "h":
            response +=\
                "```\n" +\
                pre+"help       " + pre+"h  -  " + "show this help message\n" +\
                pre+"resources  " + pre+"r  -  " + "list resources\n" +\
                "```"

        case "resources" | "r":
            if len(_botconf.botconfig.resources) == 0:
                response += "There are currently no resources"
            else:
                for r in _botconf.botconfig.resources:
                    response += "- " + str(r) + "\n"
        case _:
            response += "Unknown command. Type `" + pre+"help` for help"

    await message.channel.send(response, suppress_embeds=True)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    # Don't respond to this bot's own messages
    if message.author == client.user:
        return

    if _is_greeting(message):
        response = await llm.generate_response(
            message,
            _botconf.botconfig.system_prompt +
            "You will respond with a somewhat short greeting and mention their name. " +
            f"Their name is {message.author.name}.",
        )
        if not response is None:
            await message.reply(response)
        return

    if _is_command(message.content):
        split_message = message.content.strip(" \t\n").split()
        command = split_message[0][len(_botconf.botconfig.command_prefix):]
        args = split_message[1:]

        await _handle_command(command, args, message)
        return

    if client.user in message.mentions:
        response = await llm.generate_response(
            message,
            _botconf.botconfig.system_prompt +
            f" The user's name is {message.author.name}",
        )
        if not response is None:
            await message.reply(response)
        return
