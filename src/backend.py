from openai import OpenAI, NotFoundError, APIConnectionError
from consts import DEFAULT_EXAMPLES
from configmanager import ConfigManger

class BackendLLM:
    """
    base_url: Base url for ollama the default is `http://localhost:11434/v1`
    system_msg: The system message for the LLM
    examples (optional): The examples help it understand the game, default is `[{"role": "user", "content": '"🌍 Earth + 💧 Water"'}, {"role": "assistant", "content": '🌱 Plant'}]`
    """

    def __init__(self) -> None:
        
        self.conf_manager = ConfigManger()
        conf = self.conf_manager.get_config()
        self.base_url: str = conf["base_url"]
        self.model: str = conf["model"]
        self.simple_check()

        self.examples = DEFAULT_EXAMPLES
        self.system_msg = conf["system_msg"]

        self.__client = OpenAI(
            base_url = self.base_url,
            api_key="ollama",
        )

        self.final_examples = []

    def simple_check(self):
        if not self.base_url.endswith("/v1"):
            if self.base_url[-1] == "/":
                self.base_url += "v1"
            else:
                self.base_url += "/v1"
            self.conf_manager.set_base_url(self.base_url)

    def reload_settings(self):
        conf = self.conf_manager.get_config()
        if self.base_url != (new_base_url := conf["base_url"]):
            self.base_url = new_base_url
            self.simple_check()
            self.__client = OpenAI(
                base_url = self.base_url,
                api_key="ollama",
            )

        self.system_msg = conf["system_msg"]
        self.model = conf["model"]
        self.examples = conf["examples"]

    def convert_examples(self):
        self.final_examples.clear()
        for example in self.examples:
            self.final_examples.extend(
                [
                    {"role": "user", "content": f'"{example["from_str"].strip()}"'},
                    {"role": "assistant", "content": example["result_str"].strip()},
                ]
            )

    def generate_result(self, first: str, second: str) -> tuple[str | None, str | None]:
        if not first or not second:
            return None, "Invalid Input"
        
        # TODO: don't check it every generation.
        self.reload_settings()

        result = f'"{first} + {second}"'
        combined_input = f"{first} + {second}"
        reversed_input = f"{second} + {first}"
        print(combined_input)
        for example in DEFAULT_EXAMPLES:
            print(example['from_str'])
            if combined_input == example['from_str'] or reversed_input == example['from_str']:
                print("Found!")
                return example['result_str'], None  # Return the result from example

        result = f'"{first} + {second}"'

        self.convert_examples()
        messages = [
            {"role": "system", "content": self.system_msg},     
        ]
        messages.extend(self.final_examples)
        messages.append({"role": "user", "content": result})
        try:
            response = self.__client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=15,
                n=1,
                temperature=0,
                top_p=1,  
            )
        except NotFoundError:
            return None, "Invalid Base Url"
        except APIConnectionError:
            return None, "Connection Error, make sure ollama is running in background and try again"

        return response.choices[0].message.content, None

if __name__ == '__main__':
    llm = BackendLLM()
    print(llm.generate_result("🌊 Wave", "💧 Water"))