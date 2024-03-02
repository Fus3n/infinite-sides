import json, os

from consts import DEFAULT_BASE_URL, DEFAULT_SYSTEM_MSG, DEFAULT_MODEL, DEFAULT_EXAMPLES, DEFAULT_CHIPS

class ConfigManger:

    def __init__(self) -> None:
        self.file = "inf_config.json"
        self.init_file()

    def init_file(self):
        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump({
                    "base_url": DEFAULT_BASE_URL,
                    "system_msg": DEFAULT_SYSTEM_MSG
                }, f, indent=4)
            return
        
        with open(self.file, "r") as f:
            config = json.load(f)
            if "base_url" not in config:
                config["base_url"] = DEFAULT_BASE_URL
            if "system_msg" not in config:
                config["system_msg"] = DEFAULT_SYSTEM_MSG
            if "model" not in config:
                config["model"] = DEFAULT_MODEL
            if "examples" not in config:
                config["examples"] = DEFAULT_EXAMPLES
            if "default_chips" not in config:
                config["default_chips"] = DEFAULT_CHIPS
            self.set_config(config)

    def get_config(self):
        with open(self.file, "r") as f:
            return json.load(f)
        
    def set_config(self, config):
        with open(self.file, "w") as f:
            json.dump(config, f, indent=4, )

    def get_value(self, key):
        config = self.get_config()
        return config[key]
    
    def set_key_value(self, key, value):
        config = self.get_config()
        config[key] = value
        self.set_config(config)

    def set_base_url(self, url):
        self.set_key_value("base_url", url)
