from PySide6.QtCore import Signal, QThread
import httpx

class FetchModels(QThread):
    fetched = Signal(list)
    error = Signal(str)

    def __init__(self, client):
        super().__init__(None)
        self.client = client

    def run(self):
        try: 
            ollama_models = self.client.list()
            ollama_models = [model["name"] for model in ollama_models['models']]
            self.fetched.emit(ollama_models)
        except httpx.ConnectError as e:
            self.error.emit("Ollama is not running in the background, please make sure it is, and try again.\nIf it is running and you are still getting this, make sure your base url is correct.")
        except Exception as e:
            self.error.emit(str(e))