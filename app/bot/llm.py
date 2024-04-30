"""
Integration with LLMs
"""

import json
import requests
from requests.models import HTTPError

import globalconf

import discord

async def generate_response(message: discord.Message, system_prompt: str, auto_pull: bool = False) -> str | None:
    print(f"Generating response ...\nUser prompt:\n{message.content}\nSystem prompt:\n{system_prompt}")

    r = requests.post(
        f"http://{globalconf.LLM_HOST}:{globalconf.LLM_PORT}/api/generate",
        json={
            "model": globalconf.LLM_MODEL,
            "prompt": message.content,
            "system": system_prompt,
            "context": [],
        },
        stream=True,
    )

    try:
        r.raise_for_status()
    except HTTPError as e:
        err_res = e.response
        if not isinstance(err_res, requests.models.Response):
            raise e

        print(f"Error:\n{err_res.json()}")

        if auto_pull:
            pull_model(globalconf.LLM_MODEL)
        
        return None

    response = ""
    # While receiving responses, show typing status
    async with message.channel.typing():
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
    return response


def pull_model(model: str):
    print(f"Pulling model: {model} ...")
    r = requests.post(
        f"http://{globalconf.LLM_HOST}:{globalconf.LLM_PORT}/api/pull",
        json={
            "name": model,
            "stream": False,
        },
    )

    r.raise_for_status()
    print(r.json())
