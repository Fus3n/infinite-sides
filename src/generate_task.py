from PySide6.QtWidgets import QGraphicsTextItem
from PySide6.QtCore import Signal, QThread
from backend import BackendLLM


class GenerateTask(QThread):

    finished = Signal(QGraphicsTextItem, QGraphicsTextItem, str, str)

    def __init__(self) -> None:
        """        Initialize the object with default values for chip1, chip2, and llm.
        """

        super().__init__()
        self.chip1 = None
        self.chip2 = None
        self.llm = BackendLLM()

    def update_text(self, chip1: QGraphicsTextItem, chip2: QGraphicsTextItem):
        """        Update the text items for chip1 and chip2.

        This method updates the text items for chip1 and chip2 with the provided QGraphicsTextItem objects.

        Args:
            chip1 (QGraphicsTextItem): The QGraphicsTextItem object for chip1.
            chip2 (QGraphicsTextItem): The QGraphicsTextItem object for chip2.
        """

        self.chip1 = chip1
        self.chip2 = chip2

    def run(self):
        """        Run the task to generate a result based on the input from chip1 and chip2.

        If both chip1 and chip2 are empty, it emits a finished signal with an error message.
        Otherwise, it uses the input from chip1 and chip2 to generate a result using llm.generate_result.
        If an error occurs during the generation process, it emits a finished signal with the error message.
        Otherwise, it emits a finished signal with the result.

        Returns:
            bool: True if the task runs successfully.
        """

        if not self.chip1 and not self.chip2:
            self.finished.emit(self.chip1, self.chip2, "", "Generate task got invalid or no text")
            
        result, err = self.llm.generate_result(self.chip1.toPlainText(), self.chip2.toPlainText())
        
        if err:
            self.finished.emit(self.chip1, self.chip2, "", err)
            return

        self.finished.emit(self.chip1, self.chip2, result, err)
        return True