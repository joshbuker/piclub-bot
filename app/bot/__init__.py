import discord

from . import config as _botcfg

_intents = discord.Intents.default()
_intents.message_content = True

client = discord.Client(intents=_intents)

def _is_command(text: str) -> bool:
    return text.startswith(_botcfg.botconfig.command_prefix)


def _is_greeting(message: discord.Message) -> bool:
    has_greeting_prefix = False
    for greeting in _botcfg.botconfig.greetings:
        if message.content.lower().startswith(greeting):
            has_greeting_prefix = True
            break

    if not has_greeting_prefix:
        return False

    return client.user in message.mentions


async def _handle_command(command: str, args: list[str], message: discord.Message):
    response = ""
    pre = _botcfg.botconfig.command_prefix
    match command.lower():
        case "help" | "h":
            response +=\
                "```\n" +\
                pre+"help       " + pre+"h  -  " + "show this help message\n" +\
                pre+"resources  " + pre+"r  -  " + "list resources\n" +\
                "```"

        case "resources" | "r":
            if len(_botcfg.botconfig.resources) == 0:
                response += "There are currently no resources"
            else:
                for r in _botcfg.botconfig.resources:
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
        await message.channel.send(f"Hello {message.author.mention}")
        return

    if _is_command(message.content):
        split_message = message.content.strip(" \t\n").split()
        command = split_message[0][len(_botcfg.botconfig.command_prefix):]
        args = split_message[1:]

        await _handle_command(command, args, message)
        return

