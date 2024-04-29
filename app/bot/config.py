import yaml

class Resource:
    name: str
    link: str
    desc: str

    def __init__(self, name: str, link: str, desc: str):
        self.name = name
        if not link.startswith("https://") and not link.startswith("http://"):
            link = "https://" + link
        self.link = link
        self.desc = desc

    def __str__(self) -> str:
        s = f"[{self.name}]({self.link})"
        if self.desc != "":
            s += f": {self.desc}"
        return s


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

        if "command_prefix" in cfg_obj and isinstance(cfg_obj["command_prefix"], str):
            self.command_prefix = cfg_obj["command_prefix"]

        if "greetings" in cfg_obj and isinstance(cfg_obj["greetings"], list):
            # Make sure all elements are strings
            for e in cfg_obj["greetings"]:
                if not isinstance(e, str):
                    return

            self.greetings = cfg_obj["greetings"]

        if "resources" in cfg_obj and isinstance(cfg_obj["resources"], list):
            for res in cfg_obj["resources"]:
                if "name" not in res or "link" not in res:
                    continue

                if "desc" not in res:
                    res["desc"] = ""

                self.resources.append(
                    Resource(res["name"], res["link"], res["desc"])
                )


botconfig = BotConfig()
