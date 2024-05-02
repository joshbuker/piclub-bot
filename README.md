# PiClub-Bot

## `.env` vs `data/config.yaml`

The `.env` file is for secrets, like the Discord bot's token, the Discord guild
ID, the Ollama host, etc. Every instance of the bot will have different values
in the `.env` file.

The `data/config.yaml` file is for general config that can be shared between
different instances of the bot. You can distribute your `data/config.yaml` file
to someone else, and they will be able to run their own bot that will act pretty
much the same as yours. It will use the same LLM model, the same system prompt,
the same resource links, etc.

[Project structure](https://www.pythonbynight.com/blog/starting-python-project)
