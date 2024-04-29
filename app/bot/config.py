import yaml

class BotConfig:
    command_prefix: str
    greetings: list[str]

    def __init__(self):
        self.command_prefix = "!"
        self.greetings = ["hello", "hi", "hey"]

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
