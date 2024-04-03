# from openai import OpenAI, NotFoundError, APIConnectionError
from ollama import Client, RequestError, ChatResponse, ResponseError
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
        self.check_base_url()

        self.examples = DEFAULT_EXAMPLES
        self.system_msg = conf["system_msg"]
        self.__client = Client(
            host=self.base_url,
        )

        self.final_examples = []

    def check_base_url(self):
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
            self.check_base_url()
            self.__client = Client(
                host=self.base_url,
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
        
        self.reload_settings()
        
        result = f'"{first} + {second}"'

        self.convert_examples()
        messages = [
            {"role": "system", "content": self.system_msg},     
        ]
        messages.extend(self.final_examples)
        messages.append({"role": "user", "content": result})
        try:
            response: ChatResponse = self.__client.chat(
                model=self.model,
                messages=messages,
                stream=False,
                options={
                    "top_p": 1,
                    "temperature": 0,
                    "stop": ["[\n", "\r\n", "\n", "\"", "<|im_end|>"]
                }
            )
        except RequestError as e:
            return None, str(e)
        except ResponseError as e:
            return None, str(e)

        return response['message']['content'], None

if __name__ == '__main__':
    llm = BackendLLM()
    print(llm.generate_result("🌊 Wave", "💧 Water"))