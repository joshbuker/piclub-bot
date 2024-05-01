"""
Integration with LLMs
"""

import json
import aiohttp

import globalconf as _globalconf
from logtools import log_print
from . import botconf as _botconf

import discord

async def generate_response(
    message: discord.Message,
    system_prompt: str = _botconf.botconfig.system_prompt,
    auto_pull_model: bool = _botconf.botconfig.auto_pull_model # TODO: Use this again
) -> str | None:
    url = f"http://{_globalconf.LLM_HOST}:{_globalconf.LLM_PORT}/api/generate"
    log_print(f"url: {url}")

    # While receiving responses, show typing status
    async with message.channel.typing():
        log_print(f"Generating response ...\nUser prompt:\n{message.content}\nSystem prompt:\n{system_prompt}")

        async with aiohttp.ClientSession() as cs:
            async with cs.post(url, json={
                "model": _botconf.botconfig.llm_model,
                "prompt": message.content,
                "system": system_prompt,
                "context": [],
                "stream": False,
            }) as res:
                try:
                    data = await res.json()
                    if "error" in data:
                        log_print(f"Error: {data['error']}")
                        log_print(f"data: {json.dumps(data)}")
                        return None

                    dur = data["total_duration"] / 1_000_000_000
                    log_print(f"response took {dur:.3f} seconds")

                    return data["response"]


                except Exception as e:
                    #err_res = e.response
                    #if not isinstance(err_res, requests.models.Response):
                        #raise e

                    log_print(f"Error:\n{e}\nType: {type(e)}")

                    #if err_res.status_code == 404 and auto_pull_model:
                        #pull_model(_botconf.botconfig.llm_model)

                    return None
                #except ConnectionError as e:
                    #log_print(f"Ollama server unavailable at {url}")
                    #return None

        #response = ""
            ## Loop through tokens as they are streamed in
        #for line in r.iter_lines():
            #body = json.loads(line) # Parse response as json

            ## Append token to response
            #response_part = body.get("response", "")
            #response += response_part

            ## Raise error if present
            #if "error" in body:
                #raise Exception(body["error"])

            ## Return response if done
            #if body.get("done", False):
                #log_print("Done typing (done)")
                #return response

        #log_print("Done typing (no more lines)")

        ## Return response
        #return None


#def pull_model(model: str):
    #log_print(f"Pulling model: {model} ...")
    #r = requests.post(
        #f"http://{_globalconf.LLM_HOST}:{_globalconf.LLM_PORT}/api/pull",
        #json={
            #"name": model,
            #"stream": False,
        #},
    #)

    #r.raise_for_status()
    #log_print(r.json())
