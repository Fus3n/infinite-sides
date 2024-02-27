import json, os

from consts import DEFAULT_BASE_URL, DEFAULT_SYSTEM_MSG, DEFAULT_MODEL, DEFAULT_EXAMPLES

class ConfigManger:

    def __init__(self) -> None:
        """        Initialize the object with default file name and initialize the file.

        This method initializes the object with a default file name "inf_config.json" and then calls the init_file method to initialize the file.

        Args:
            self: The object itself.
        """

        self.file = "inf_config.json"
        self.init_file()

    def init_file(self):
        """        Initialize the configuration file with default values if it does not exist,
        or load the existing configuration and set default values for missing keys.

        If the file does not exist, it creates a new file with default values for "base_url" and "system_msg".
        If the file exists, it loads the configuration and sets default values for missing keys: "base_url", "system_msg", "model", and "examples".
        """

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
            self.set_config(config)

    def get_config(self):
        """        Get the configuration from the specified file.

        Reads the content of the file using JSON format and returns the configuration.

        Returns:
            dict: The configuration data loaded from the file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            JSONDecodeError: If the content of the file is not a valid JSON format.
        """

        with open(self.file, "r") as f:
            return json.load(f)
        
    def set_config(self, config):
        """        Set the configuration settings to a file.

        This function takes a configuration dictionary and writes it to a file in JSON format with an indentation of 4 spaces.

        Args:
            config (dict): A dictionary containing the configuration settings.


        Raises:
            IOError: If an error occurs while writing to the file.
        """

        with open(self.file, "w") as f:
            json.dump(config, f, indent=4, )

    def get_key(self, key):
        """        Get the value corresponding to the given key from the configuration.

        Args:
            key (str): The key for which the value needs to be retrieved from the configuration.

        Returns:
            Any: The value corresponding to the given key from the configuration.

        Raises:
            KeyError: If the given key is not present in the configuration.
        """

        config = self.get_config()
        return config[key]
    
    def set_key(self, key, value):
        """        Set a key-value pair in the configuration.

        This function sets a key-value pair in the configuration dictionary and updates the configuration.

        Args:
            key (str): The key to be set in the configuration.
            value (any): The value to be associated with the key in the configuration.
        """

        config = self.get_config()
        config[key] = value
        self.set_config(config)

    def set_base_url(self, url):
        """        Set the base URL for the API client.

        This method sets the base URL for the API client to be used for making requests.

        Args:
            url (str): The base URL to be set for the API client.
        """

        self.set_key("base_url", url)
