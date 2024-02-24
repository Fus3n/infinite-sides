from openai import OpenAI
from consts import ExampleType, DEFAULT_EXAMPLES
from configmanager import ConfigManger

class BackendLLM:
    """
    base_url: Base url for ollama the default is `http://localhost:11434/v1`
    system_msg: The system message for the LLM
    examples (optional): The examples help it understand the game, default is `[{"role": "user", "content": '"🌍 Earth + 💧 Water"'}, {"role": "assistant", "content": '🌱 Plant'}]`
    """

    def __init__(self) -> None:
        
        conf = ConfigManger().get_config()
        self.base_url = conf["base_url"]
        self.examples = DEFAULT_EXAMPLES
        self.system_msg = conf["system_msg"]

        self.__client = OpenAI(
            base_url = self.base_url,
            api_key="ollama",
        )

    def generate_result(self, first: str, second: str, model = "llama2"):
        result = f'"{first} + {second}"'

        messages = [
            {"role": "system", "content": self.system_msg},     
        ]
        messages.extend(self.examples)
        messages.append({"role": "user", "content": result})

        response = self.__client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=15,
            n=1,
            temperature=0,
            top_p=1,  
        )
        print(response.choices[0].message.content)

        return response.choices[0].message.content

if __name__ == '__main__':
    llm = BackendLLM()
    print(llm.generate_result("🌊 Wave", "💧 Water"))