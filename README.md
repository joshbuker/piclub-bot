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

## Install Nvidia Container Toolkit

https://hub.docker.com/r/ollama/ollama

1. Configure the repository

```sh
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
    | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
    | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
    | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
```

2. Install the NVIDIA Container Toolkit packages

```sh
sudo apt-get install -y nvidia-container-toolkit
```

3. Configure Docker to use Nvidia driver

```sh
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```
