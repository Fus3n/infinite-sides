from PySide6.QtWidgets import QGraphicsTextItem
from PySide6.QtCore import Signal, QThread
from backend import BackendLLM


class GenerateTask(QThread):

    finished = Signal(QGraphicsTextItem, QGraphicsTextItem, str)

    def __init__(self) -> None:
        super().__init__()
        self.chip1 = None
        self.chip2 = None
        self.llm = BackendLLM()

    def update_text(self, chip1: QGraphicsTextItem, chip2: QGraphicsTextItem):
        self.chip1 = chip1
        self.chip2 = chip2

    def run(self):
        if not self.chip1 and not self.chip2:
            raise Exception("Generate task got invalid or no text")
            
        result = self.llm.generate_result(self.chip1.toPlainText(), self.chip2.toPlainText())
        print("Result", result)
        self.finished.emit(self.chip1, self.chip2, result)
        return True