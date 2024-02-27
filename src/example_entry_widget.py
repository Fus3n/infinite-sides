from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout, 
    QLineEdit, 
    QPushButton
)

class ExampleEntry(QFrame):

    def __init__(self, from_text: str, result_text: str, item) -> None:
        """        Initialize the class instance with input and result text along with an item.

        Args:
            from_text (str): The input text.
            result_text (str): The result text.
            item: The item associated with the instance.
        """

        super().__init__()
        self.item = item
        self.from_text = from_text
        self.result_text = result_text


        lay = QHBoxLayout()

        self.from_input = QLineEdit(self.from_text)
        self.result_input = QLineEdit(self.result_text)
        self.result_input.setMaximumWidth(100)
        dlt_btn = QPushButton("X")
        dlt_btn.setMinimumWidth(20)
        dlt_btn.clicked.connect(self.remove_item)

        lay.addWidget(self.from_input, stretch=2)
        lay.addWidget(self.result_input, stretch=1)
        lay.addWidget(dlt_btn)

        self.setLayout(lay)

    def remove_item(self):
        """        Remove the item from the list widget.

        This method removes the item from the list widget by taking its index and removing it from the list.
        """

        l = self.item.listWidget()
        it = l.row(self.item)
        l.takeItem(it)