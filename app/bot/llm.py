"""
Integration with LLMs
"""

import json
import requests
from requests.exceptions import (
    HTTPError,
    ConnectionError,
)

import globalconf as _globalconf
from . import botconf as _botconf

import discord

async def generate_response(
    message: discord.Message,
    system_prompt: str = _botconf.botconfig.system_prompt,
    auto_pull_model: bool = _botconf.botconfig.auto_pull_model
) -> str | None:
    # While receiving responses, show typing status
    async with message.channel.typing():

        print(f"Generating response ...\nUser prompt:\n{message.content}\nSystem prompt:\n{system_prompt}")

        url = f"http://{_globalconf.LLM_HOST}:{_globalconf.LLM_PORT}/api/generate"

        try:
            r = requests.post(
                url,
                json={
                    "model": _globalconf.LLM_MODEL,
                    "prompt": message.content,
                    "system": system_prompt,
                    "context": [],
                },
                stream=True,
            )

            r.raise_for_status()
        except HTTPError as e:
            err_res = e.response
            if not isinstance(err_res, requests.models.Response):
                raise e

            print(f"Error:\n{err_res.json()}")

            if err_res.status_code == 404 and auto_pull_model:
                pull_model(_globalconf.LLM_MODEL)

            return None
        except Exception as e:
            print(f"Ollama server unavailable at {url}")
            return None

        response = ""
            # Loop through tokens as they are streamed in
        for line in r.iter_lines():
            body = json.loads(line) # Parse response as json

            # Append token to response
            response_part = body.get("response", "")
            response += response_part

            # Raise error if present
            if "error" in body:
                raise Exception(body["error"])

            # Return response if done
            if body.get("done", False):
                return response

        # Return response
        return None


def pull_model(model: str):
    print(f"Pulling model: {model} ...")
    r = requests.post(
        f"http://{_globalconf.LLM_HOST}:{_globalconf.LLM_PORT}/api/pull",
        json={
            "name": model,
            "stream": False,
        },
    )

    r.raise_for_status()
    print(r.json())
