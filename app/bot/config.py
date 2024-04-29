import yaml

class Resource:
    name: str
    link: str
    desc: str

    def __init__(self, name: str, link: str, desc: str):
        self.name = name
        self.link = link
        self.desc = desc

    def __str__(self) -> str:
        return f"[{self.name}]({self.link}): {self.desc}"


class BotConfig:
    command_prefix: str
    greetings: list[str]
    resources: list[Resource]

    def __init__(self):
        self.command_prefix = "!"
        self.greetings = ["hello", "hi", "hey"]
        self.resources = []

    def load_from_file(self, f):
        cfg_obj = yaml.load(f, yaml.Loader)

        if hasattr(cfg_obj, "command_prefix") and isinstance(cfg_obj.command_prefix, str):
            self.command_prefix = cfg_obj.command_prefix

        if hasattr(cfg_obj, "greetings") and isinstance(cfg_obj.greetings, list):
            # Make sure all elements are strings
            for e in cfg_obj.greetings:
                if not isinstance(e, str):
                    return

            self.greetings = cfg_obj.greetings

botconfig = BotConfig()
